# 1. Bibliotecas de terceiros (FastAPI e SQLAlchemy)
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
import json
import os

# 2. Módulos locais do projeto
import models
import schemas
import crud
import auth
from database import engine, get_db
from datetime import datetime

# 3. IA
from ia import treinar_modelo, prever_tempo_espera, modelo_disponivel

# 4. Anonimização
from anonimizacao import exportar_dados_anonimizados

# ==============================================
# INICIALIZAÇÃO
# ==============================================

# Criar as tabelas no PostgreSQL ao arrancar
models.Base.metadata.create_all(bind=engine)

# Instância da aplicação
app = FastAPI(
    title="S.U.H. - Sistema de Urgências Hospitalares",
    description="Módulo Backend e API de Gestão Clínica"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "chave-local-desenvolvimento-nao-usar-em-producao")
)

templates = Jinja2Templates(directory="templates")

# Gestão de sessão em memória (desenvolvimento)
session_store = {}

def get_session(request: Request):
    username = request.cookies.get("session_username")
    if username and username in session_store:
        return session_store[username]
    return None

# ==============================================
# HOMEPAGE (Frontend Híbrido mínimo)
# ==============================================

@app.get("/", response_class=HTMLResponse, tags=["Interface"])
async def homepage():
    html_content = """
    <html>
        <head>
            <title>SIAGUH - Sistema de Urgências</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 50px; background-color: #f4f7f6; }
                .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }
                h1 { color: #2c3e50; }
                .status-online { color: #27ae60; font-weight: bold; }
                .btn { background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏥 SIAGUH</h1>
                <p class="status-online">● Sistema Online e Base de Dados Conectada</p>
                <hr>
                <p>Módulos Ativos: Admissão, Triagem, Gestão Clínica, IA, Anonimização</p>
                <br>
                <a href="/docs" class="btn">Aceder à API (Swagger)</a>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ==============================================
# AUTENTICAÇÃO
# ==============================================

@app.post("/auth/login", response_model=schemas.Token, tags=["Autenticação"])
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.Utilizador).filter(models.Utilizador.username == login_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not auth.verify_password(login_data.password, user.passwordhash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = auth.create_access_token(data={"sub": user.username})
    return schemas.Token(access_token=access_token, token_type="bearer", idperfil=user.idperfil, username=user.username)

@app.get("/auth/me", tags=["Autenticação"])
def read_current_user(current_user: models.Utilizador = Depends(auth.get_current_user)):
    return {"idutilizador": current_user.idutilizador, "username": current_user.username, "idperfil": current_user.idperfil}

# ==============================================
# ROTAS PARA UTENTES
# ==============================================

@app.post("/utentes/", response_model=schemas.Utente, tags=["Admissão"])
def criar_utente(utente: schemas.UtenteCreate, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_rececionista_ou_admin)):
    db_utente = crud.get_utente(db, numutente=utente.numutente)
    if db_utente:
        raise HTTPException(status_code=400, detail=f"Utente {utente.numutente} já registado.")
    return crud.create_utente(db=db, utente=utente)

@app.get("/utentes/", response_model=list[schemas.Utente], tags=["Admissão"])
def listar_utentes(db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    return crud.get_all_utentes(db)

@app.get("/utentes/{numutente}", response_model=schemas.Utente, tags=["Admissão"])
def ler_utente(numutente: int, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    db_utente = crud.get_utente(db, numutente=numutente)
    if db_utente is None:
        raise HTTPException(status_code=404, detail="Utente não encontrado.")
    return db_utente

# ==============================================
# ROTAS PARA HOSPITAIS
# ==============================================

@app.post("/hospitais/", response_model=schemas.Hospital, tags=["Configuração"])
def criar_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_admin)):
    db_hospital = crud.get_hospital(db, nomehosp=hospital.nomehosp)
    if db_hospital:
        raise HTTPException(status_code=400, detail="Hospital já configurado.")
    return crud.create_hospital(db=db, hospital=hospital)

@app.get("/hospitais/", response_model=list[schemas.Hospital], tags=["Configuração"])
def listar_hospitais(db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    return crud.get_all_hospitais(db)

# ==============================================
# ROTAS PARA EPISÓDIOS
# ==============================================

@app.post("/episodios/", response_model=schemas.Episodio, tags=["Episódios"])
def criar_episodio(episodio: schemas.EpisodioCreate, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_rececionista_ou_admin)):
    db_hosp = db.query(models.Hospital).filter(models.Hospital.nomehosp == episodio.nomehosp).first()
    if not db_hosp:
        raise HTTPException(status_code=404, detail=f"Hospital '{episodio.nomehosp}' não existe.")
    db_utente = db.query(models.Utente).filter(models.Utente.numutente == episodio.numutente).first()
    if not db_utente:
        raise HTTPException(status_code=404, detail=f"Utente {episodio.numutente} não encontrado.")
    return crud.criar_episodio(db=db, episodio=episodio)

@app.get("/episodios/", response_model=list[schemas.Episodio], tags=["Episódios"])
def listar_episodios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obter_episodios(db=db, skip=skip, limit=limit)

@app.get("/episodios/{numepis}", response_model=schemas.Episodio, tags=["Episódios"])
def ler_episodio(numepis: int, db: Session = Depends(get_db)):
    db_episodio = crud.obter_episodio_por_id(db=db, numepis=numepis)
    if not db_episodio:
        raise HTTPException(status_code=404, detail=f"Episódio {numepis} não encontrado.")
    return db_episodio

@app.put("/episodios/{numepis}/encerrar", response_model=schemas.Episodio, tags=["Episódios"])
def encerrar_episodio(numepis: int, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_medico)):
    try:
        return crud.encerrar_episodio(db=db, numepis=numepis)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==============================================
# ROTAS PARA TRIAGEM
# ==============================================

@app.post("/triagens/", response_model=schemas.TriagemOut, tags=["Triagem"])
def criar_triagem(triagem: schemas.TriagemCreate, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_enfermeiro)):
    try:
        return crud.create_triagem(db=db, triagem=triagem)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/triagens/", response_model=list[schemas.TriagemOut], tags=["Triagem"])
def listar_triagens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    return crud.get_all_triagens(db=db, skip=skip, limit=limit)

@app.get("/triagens/{numepis}", response_model=schemas.TriagemOut, tags=["Triagem"])
def obter_triagem_por_episodio(numepis: int, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    triagem = crud.get_triagem_by_episodio(db=db, numepis=numepis)
    if not triagem:
        raise HTTPException(status_code=404, detail=f"Triagem para episódio {numepis} não encontrada")
    return triagem

# ==============================================
# ROTAS PARA ATO MÉDICO
# ==============================================

@app.post("/atos/", response_model=schemas.AtoOut, tags=["Ato Médico"])
def criar_ato(ato: schemas.AtoCreate, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_medico)):
    try:
        return crud.create_ato(db=db, ato=ato)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/atos/", response_model=list[schemas.AtoOut], tags=["Ato Médico"])
def listar_atos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    return crud.get_all_atos(db=db, skip=skip, limit=limit)

@app.get("/atos/episodio/{numepis}", response_model=list[schemas.AtoOut], tags=["Ato Médico"])
def obter_atos_por_episodio(numepis: int, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    return crud.get_atos_by_episodio(db=db, numepis=numepis)

@app.get("/atos/{idato}", response_model=schemas.AtoOut, tags=["Ato Médico"])
def obter_ato_por_id(idato: int, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    ato = crud.get_ato_by_id(db=db, idato=idato)
    if not ato:
        raise HTTPException(status_code=404, detail=f"Ato médico {idato} não encontrado")
    return ato

# ==============================================
# ROTAS PARA PRESCRIÇÕES
# ==============================================

@app.post("/prescricoes/", response_model=schemas.PrescricaoOut, tags=["Prescrições"])
def criar_prescricao(prescricao: schemas.PrescricaoCreate, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_medico)):
    try:
        return crud.create_prescricao(db=db, prescricao=prescricao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/prescricoes/", response_model=list[schemas.PrescricaoOut], tags=["Prescrições"])
def listar_prescricoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    return crud.get_all_prescricoes(db=db, skip=skip, limit=limit)

@app.get("/prescricoes/episodio/{numepis}", response_model=list[schemas.PrescricaoOut], tags=["Prescrições"])
def obter_prescricoes_por_episodio(numepis: int, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    return crud.get_prescricoes_by_episodio(db=db, numepis=numepis)

# ==============================================
# ROTAS PARA INTERNAMENTO
# ==============================================

@app.post("/internamentos/", response_model=schemas.InternamentoOut, tags=["Internamento"])
def criar_internamento(internamento: schemas.InternamentoCreate, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_medico)):
    try:
        return crud.create_internamento(db=db, internamento=internamento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/internamentos/", response_model=list[schemas.InternamentoOut], tags=["Internamento"])
def listar_internamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    return crud.get_all_internamentos(db=db, skip=skip, limit=limit)

@app.get("/internamentos/{numepis}", response_model=schemas.InternamentoOut, tags=["Internamento"])
def obter_internamento_por_episodio(numepis: int, db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    internamento = crud.get_internamento_by_episodio(db=db, numepis=numepis)
    if not internamento:
        raise HTTPException(status_code=404, detail=f"Internamento para episódio {numepis} não encontrado")
    return internamento

# ==============================================
# ROTAS PARA IA
# ==============================================

@app.get("/ia/status", tags=["IA"])
def ia_status():
    return {"modelo_disponivel": modelo_disponivel(), "modelo_tipo": "RandomForestRegressor" if modelo_disponivel() else None}

@app.post("/ia/treinar", tags=["IA"])
def treinar(db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    if current_user.idperfil not in [1, 4]:
        raise HTTPException(status_code=403, detail="Acesso restrito a Médicos e Administradores")
    modelo, metricas = treinar_modelo(db=db, force_retrain=True)
    if modelo is None:
        raise HTTPException(status_code=400, detail="Dados insuficientes para treino (mínimo 10 episódios encerrados com triagem)")
    return {"mensagem": "Modelo treinado com sucesso", "metricas": metricas}

@app.get("/ia/tempo-espera", tags=["IA"])
def obter_tempo_espera(prioridade: int, hora: int, dia_semana: int, current_user: models.Utilizador = Depends(auth.get_current_user)):
    if prioridade < 1 or prioridade > 5:
        raise HTTPException(status_code=400, detail="prioridade deve estar entre 1 e 5")
    if hora < 0 or hora > 23:
        raise HTTPException(status_code=400, detail="hora deve estar entre 0 e 23")
    if dia_semana < 0 or dia_semana > 6:
        raise HTTPException(status_code=400, detail="dia_semana deve estar entre 0 e 6")
    prioridade_texto = {1: "Imediata (Vermelho)", 2: "Muito Urgente (Laranja)", 3: "Urgente (Amarelo)", 4: "Pouco Urgente (Verde)", 5: "Não Urgente (Azul)"}
    resultado = prever_tempo_espera(prioridade, hora, dia_semana)
    return {"prioridade": prioridade, "prioridade_texto": prioridade_texto.get(prioridade, "Desconhecida"), "hora": hora, "dia_semana": dia_semana, **resultado}

# ==============================================
# ROTA PARA EXPORTAÇÃO ANONIMIZADA
# ==============================================

# ==============================================
# ROTAS HTML — FRONTEND
# ==============================================

PERFIL_NOME = {1: "Médico", 2: "Enfermeiro", 3: "Rececionista", 4: "Administrador"}

@app.get("/login", response_class=HTMLResponse, tags=["Frontend"])
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None, "utilizadores": None})

@app.post("/login", response_class=HTMLResponse, tags=["Frontend"])
async def login_form(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    user = db.query(models.Utilizador).filter(models.Utilizador.username == username).first()
    if not user or not auth.verify_password(password, user.passwordhash):
        utilizadores = db.query(models.Utilizador).order_by(models.Utilizador.idperfil).all()
        return templates.TemplateResponse(request, "login.html", {
            "error": "Credenciais inválidas",
            "utilizadores": utilizadores,
            "perfil_nome": PERFIL_NOME
        })
    session_store[username] = {"username": username, "idperfil": user.idperfil}
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session_username", value=username)
    return response

@app.get("/logout", tags=["Frontend"])
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session_username")
    return response

@app.get("/dashboard", response_class=HTMLResponse, tags=["Frontend"])
def dashboard(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    stats = {
        "episodios": db.query(models.Episodio).count(),
        "utentes": db.query(models.Utente).count(),
        "triagens": db.query(models.Triagem).count(),
    }
    perfil = session["idperfil"]
    if perfil == 3:
        template = "rececionista_dashboard.html"
    elif perfil == 2:
        template = "enfermeiro_dashboard.html"
    elif perfil == 1:
        template = "medico_dashboard.html"
    else:
        template = "admin_dashboard.html"
    utentes = db.query(models.Utente).all()
    hospitais = db.query(models.Hospital).all()
    episodios = db.query(models.Episodio).filter(models.Episodio.idestadoatual != 5).order_by(models.Episodio.datahorainicio.desc()).limit(20).all()
    enfermeiros = db.query(models.Enfermeiro).all()
    medicos = db.query(models.Medico).all()
    tipos_ato = db.query(models.TipoAto).all()
    return templates.TemplateResponse(request, template, {
        "session": session, "stats": stats,
        "utentes": utentes, "hospitais": hospitais, "episodios": episodios,
        "enfermeiros": enfermeiros, "medicos": medicos, "tipos_ato": tipos_ato,
        "mensagem": request.query_params.get("mensagem"),
        "erro": request.query_params.get("erro"),
    })

@app.post("/painel/utente", tags=["Frontend"])
async def criar_utente_form(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    form = await request.form()
    try:
        utente = schemas.UtenteCreate(
            numutente=int(form.get("numutente")),
            nome=form.get("nome"), apelido=form.get("apelido"),
            localidade=form.get("localidade"), sexo=form.get("sexo"),
            datanasc=form.get("datanasc")
        )
        crud.create_utente(db=db, utente=utente)
        return RedirectResponse(url="/dashboard?mensagem=Utente+registado+com+sucesso", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/dashboard?erro={str(e)}", status_code=303)

@app.post("/painel/episodio", tags=["Frontend"])
async def criar_episodio_form(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    form = await request.form()
    try:
        episodio = schemas.EpisodioCreate(
            nomehosp=form.get("nomehosp"),
            numutente=int(form.get("numutente")),
            idestadoatual=1
        )
        crud.criar_episodio(db=db, episodio=episodio)
        return RedirectResponse(url="/dashboard?mensagem=Episodio+aberto+com+sucesso", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/dashboard?erro={str(e)}", status_code=303)

@app.post("/painel/triagem", tags=["Frontend"])
async def criar_triagem_form(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    form = await request.form()
    try:
        triagem = schemas.TriagemCreate(
            numepis=int(form.get("numepis")),
            enfnumfunc=int(form.get("enfnumfunc")),
            idprioridade_cor=int(form.get("idprioridade_cor")),
            sintomas=form.get("sintomas"),
            tensaoarterial=form.get("tensaoarterial"),
            temperatura=float(form.get("temperatura")) if form.get("temperatura") else None
        )
        crud.create_triagem(db=db, triagem=triagem)
        return RedirectResponse(url="/dashboard?mensagem=Triagem+registada+com+sucesso", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/dashboard?erro={str(e)}", status_code=303)

@app.post("/painel/ato", tags=["Frontend"])
async def criar_ato_form(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    form = await request.form()
    try:
        from datetime import datetime
        ato = schemas.AtoCreate(
            numepis=int(form.get("numepis")),
            mednumfunc=int(form.get("mednumfunc")),
            idtipoato=int(form.get("idtipoato")),
            datahorainic=datetime.now(),
            datahorafim=None
        )
        crud.create_ato(db=db, ato=ato)
        return RedirectResponse(url="/dashboard?mensagem=Ato+medico+registado+com+sucesso", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/dashboard?erro={str(e)}", status_code=303)

@app.post("/painel/prescricao", tags=["Frontend"])
async def criar_prescricao_form(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    form = await request.form()
    try:
        prescricao = schemas.PrescricaoCreate(
            numepis=int(form.get("numepis")),
            mednumfunc=int(form.get("mednumfunc")),
            medicamento=form.get("medicamento"),
            dosagem=form.get("dosagem"),
            frequencia=form.get("frequencia"),
            duracao=form.get("duracao")
        )
        crud.create_prescricao(db=db, prescricao=prescricao)
        return RedirectResponse(url="/dashboard?mensagem=Prescricao+registada+com+sucesso", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/dashboard?erro={str(e)}", status_code=303)

@app.post("/painel/alta/{numepis}", tags=["Frontend"])
def dar_alta_form(numepis: int, request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    try:
        crud.encerrar_episodio(db=db, numepis=numepis)
        return RedirectResponse(url="/dashboard?mensagem=Alta+registada+com+sucesso", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/dashboard?erro={str(e)}", status_code=303)

@app.get("/painel/utente", response_class=HTMLResponse, tags=["Frontend"])
def estado_utente(request: Request, numutente: int = None, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    if not numutente:
        return RedirectResponse(url="/dashboard", status_code=303)
    utente = db.query(models.Utente).filter(models.Utente.numutente == numutente).first()
    if not utente:
        return RedirectResponse(url="/dashboard?erro=Utente+nao+encontrado", status_code=303)
    episodios = db.query(models.Episodio).filter(
        models.Episodio.numutente == numutente
    ).order_by(models.Episodio.datahorainicio.desc()).all()
    detalhe_episodios = []
    for ep in episodios:
        triagem = db.query(models.Triagem).filter(models.Triagem.numepis == ep.numepis).first()
        atos = db.query(models.Ato).filter(models.Ato.numepis == ep.numepis).all()
        prescricoes = db.query(models.Prescricao).filter(models.Prescricao.numepis == ep.numepis).all()
        internamento = db.query(models.Internamento).filter(models.Internamento.numepis == ep.numepis).first()
        detalhe_episodios.append({
            "episodio": ep, "triagem": triagem,
            "atos": atos, "prescricoes": prescricoes, "internamento": internamento
        })
    return templates.TemplateResponse(request, "utente_estado.html", {
        "session": session, "utente": utente, "detalhe_episodios": detalhe_episodios
    })

@app.get("/ia", response_class=HTMLResponse, tags=["Frontend"])
def ia_page(request: Request):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(request, "ia.html", {"session": session, "resultado": None})

@app.get("/ia/prever", response_class=HTMLResponse, tags=["Frontend"])
def ia_prever_page(request: Request, prioridade: int, hora: int, dia_semana: int):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    resultado = prever_tempo_espera(prioridade, hora, dia_semana)
    prioridade_texto = {1: "Imediata (Vermelho)", 2: "Muito Urgente (Laranja)", 3: "Urgente (Amarelo)", 4: "Pouco Urgente (Verde)", 5: "Não Urgente (Azul)"}
    resultado["prioridade_texto"] = prioridade_texto.get(prioridade, "Desconhecida")
    resultado["hora"] = hora
    return templates.TemplateResponse(request, "ia.html", {"session": session, "resultado": resultado})

@app.get("/exportar", response_class=HTMLResponse, tags=["Frontend"])
def exportar_page(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    dados_json = exportar_dados_anonimizados(db=db, formato="json")
    dados = json.loads(dados_json)
    return templates.TemplateResponse(request, "exportar.html", {"session": session, "dados_preview": dados[:5], "total": len(dados)})

@app.post("/painel/funcionario", tags=["Frontend"])
async def criar_funcionario_form(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session or session["idperfil"] != 4:
        return RedirectResponse(url="/login", status_code=303)
    form = await request.form()
    try:
        username = form.get("username")
        password = form.get("password")
        idperfil = int(form.get("idperfil"))
        existe = db.query(models.Utilizador).filter(models.Utilizador.username == username).first()
        if existe:
            return RedirectResponse(url="/dashboard?erro=Username+ja+existe", status_code=303)
        novo_user = models.Utilizador(
            username=username,
            passwordhash=auth.get_password_hash(password),
            idperfil=idperfil
        )
        db.add(novo_user)
        db.commit()
        db.refresh(novo_user)
        novo_func = models.Funcionario(
            nome=form.get("nome"), apelido=form.get("apelido"),
            sexo=form.get("sexo"), nomehosp=form.get("nomehosp"),
            idutilizador=novo_user.idutilizador
        )
        db.add(novo_func)
        db.commit()
        db.refresh(novo_func)
        if idperfil == 1:
            db.add(models.Medico(
                mednumfunc=novo_func.idfuncionario,
                especialidade=form.get("especialidade", "Geral"),
                estagiario=form.get("estagiario") == "on"
            ))
        elif idperfil == 2:
            db.add(models.Enfermeiro(
                enfnumfunc=novo_func.idfuncionario,
                grau=form.get("grau", "Generalista")
            ))
        db.commit()
        return RedirectResponse(url="/dashboard?mensagem=Funcionario+criado+com+sucesso", status_code=303)
    except Exception as e:
        return RedirectResponse(url=f"/dashboard?erro={str(e)}", status_code=303)

@app.post("/painel/treinar-ia", tags=["Frontend"])
def treinar_ia_form(request: Request, db: Session = Depends(get_db)):
    session = get_session(request)
    if not session:
        return RedirectResponse(url="/login", status_code=303)
    modelo, metricas = treinar_modelo(db=db, force_retrain=True)
    if modelo is None:
        return RedirectResponse(url="/dashboard?erro=Dados+insuficientes+para+treino", status_code=303)
    return RedirectResponse(url=f"/dashboard?mensagem=Modelo+treinado+MAE={metricas['mae_minutos']}min", status_code=303)

# ==============================================
# EXPORTAÇÃO ANONIMIZADA (API)
# ==============================================

@app.get("/exportar/anonimizado", tags=["Exportação"])
def exportar_dados_anonimizados_endpoint(formato: str = "json", db: Session = Depends(get_db), current_user: models.Utilizador = Depends(auth.get_current_user)):
    try:
        dados = exportar_dados_anonimizados(db=db, formato=formato)
        if formato.lower() == "csv":
            return Response(content=dados, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=dados_anonimizados.csv"})
        else:
            return Response(content=dados, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na exportação: {str(e)}")
                            