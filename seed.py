from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import auth
from datetime import date
from datetime import datetime, timedelta   # seccão 6 - IA
import random                              # secção 6 - IA

# Garante que as tabelas existem na Base de Dados antes de correr
Base.metadata.create_all(bind=engine)

def povoar_sistema():
    db: Session = SessionLocal()
    try:
        print("====== A INICIAR POVOAMENTO (SEED) ======")

        # 1. CRIAR HOSPITAIS PILOTO
        hospitais_para_criar = [
            {"nomehosp": "Hospital PRODIGI Central", "localizacao": "Lisboa, Portugal"},
            {"nomehosp": "Hospital PRODIGI Norte", "localizacao": "Porto, Portugal"},
        ]

        for dados_hosp in hospitais_para_criar:
            existe_hosp = db.query(models.Hospital).filter(
                models.Hospital.nomehosp == dados_hosp["nomehosp"]
            ).first()
            if not existe_hosp:
                novo_hosp = models.Hospital(**dados_hosp)
                db.add(novo_hosp)
                print(f"Hospital '{dados_hosp['nomehosp']}' criado com sucesso.")
            else:
                print(f"Hospital '{dados_hosp['nomehosp']}' já existia.")

        db.commit()

        # 2. CRIAR UTENTES PILOTO
        utentes_para_criar = [
            {"numutente": 100001, "nome": "João", "apelido": "Silva", "localidade": "Lisboa", "sexo": "M", "datanasc": date(1990, 5, 15)},
            {"numutente": 100002, "nome": "Ana", "apelido": "Santos", "localidade": "Porto", "sexo": "F", "datanasc": date(1985, 8, 22)},
            {"numutente": 100003, "nome": "Pedro", "apelido": "Costa", "localidade": "Coimbra", "sexo": "M", "datanasc": date(1998, 12, 1)},
            {"numutente": 100004, "nome": "Maria", "apelido": "Ferreira", "localidade": "Braga", "sexo": "F", "datanasc": date(1972, 3, 8)},
            {"numutente": 100005, "nome": "Rui", "apelido": "Oliveira", "localidade": "Faro", "sexo": "M", "datanasc": date(2005, 11, 20)},
            {"numutente": 100006, "nome": "Carla", "apelido": "Rodrigues", "localidade": "Setúbal", "sexo": "F", "datanasc": date(1965, 7, 14)},
            {"numutente": 100007, "nome": "Tiago", "apelido": "Alves", "localidade": "Aveiro", "sexo": "M", "datanasc": date(1993, 9, 30)},
            {"numutente": 100008, "nome": "Sofia", "apelido": "Martins", "localidade": "Évora", "sexo": "F", "datanasc": date(1980, 2, 5)},
        ]

        for dados_utente in utentes_para_criar:
            existe_utente = db.query(models.Utente).filter(models.Utente.numutente == dados_utente["numutente"]).first()
            if not existe_utente:
                novo_utente = models.Utente(**dados_utente)
                db.add(novo_utente)
                print(f"Utente {dados_utente['numutente']} ({dados_utente['nome']}) criado com sucesso.")
            else:
                print(f"Utente {dados_utente['numutente']} já se encontrava registado.")

        db.commit()

        # 3. CRIAR UTILIZADORES PARA TESTE (Médico e Enfermeiro)
        print("\n--- A CRIAR UTILIZADORES ---")

        utilizadores_para_criar = [
            {
                "username": "dr.silva",
                "password": "medico123",
                "idperfil": 1,
                "perfil_nome": "Médico"
            },
            {
                "username": "enf.ana",
                "password": "enfermeiro123",
                "idperfil": 2,
                "perfil_nome": "Enfermeiro"
            },
            {
                "username": "rec.joao",
                "password": "rececao123",
                "idperfil": 3,
                "perfil_nome": "Rececionista"
            },
            {
                "username": "admin",
                "password": "admin123",
                "idperfil": 4,
                "perfil_nome": "Administrador"
            }
        ]

        for dados_utilizador in utilizadores_para_criar:
            existe = db.query(models.Utilizador).filter(
                models.Utilizador.username == dados_utilizador["username"]
            ).first()
            
            if not existe:
                password_hash = auth.get_password_hash(dados_utilizador["password"])
                novo_utilizador = models.Utilizador(
                    username=dados_utilizador["username"],
                    passwordhash=password_hash,
                    idperfil=dados_utilizador["idperfil"]
                )
                db.add(novo_utilizador)
                print(f"Utilizador '{dados_utilizador['username']}' ({dados_utilizador['perfil_nome']}) criado com sucesso.")
            else:
                print(f"Utilizador '{dados_utilizador['username']}' já existia.")

        db.commit()

        # 1.5 CRIAR TIPOS DE ATO (Lookup table)
        print("\n--- A CRIAR TIPOS DE ATO ---")
        
        tipos_ato_para_criar = [
            {"idtipoato": 1, "designacao": "Consulta"},
            {"idtipoato": 2, "designacao": "Exame"},
            {"idtipoato": 3, "designacao": "Procedimento"},
            {"idtipoato": 4, "designacao": "Outro"}
        ]
        
        for dados_tipo in tipos_ato_para_criar:
            existe = db.query(models.TipoAto).filter(
                models.TipoAto.idtipoato == dados_tipo["idtipoato"]
            ).first()
            if not existe:
                novo_tipo = models.TipoAto(**dados_tipo)
                db.add(novo_tipo)
                print(f"Tipo de ato '{dados_tipo['designacao']}' criado com sucesso.")
            else:
                print(f"Tipo de ato '{dados_tipo['designacao']}' já existia.")
        
        db.commit()

        # 4. CRIAR FUNCIONÁRIOS E ENFERMEIROS PARA TESTE
        print("\n--- A CRIAR FUNCIONÁRIOS E ENFERMEIROS ---")
        
        user_enf = db.query(models.Utilizador).filter(models.Utilizador.username == "enf.ana").first()
        
        if user_enf:
            funcionario_exists = db.query(models.Funcionario).filter(
                models.Funcionario.idutilizador == user_enf.idutilizador
            ).first()
            
            if not funcionario_exists:
                novo_func = models.Funcionario(
                    nome="Ana",
                    apelido="Santos",
                    sexo="F",
                    nomehosp="Hospital PRODIGI Central",
                    idutilizador=user_enf.idutilizador
                )
                db.add(novo_func)
                db.commit()
                db.refresh(novo_func)
                
                novo_enf = models.Enfermeiro(
                    enfnumfunc=novo_func.idfuncionario,
                    grau="Especialista"
                )
                db.add(novo_enf)
                db.commit()
                print(f"Enfermeiro criado com enfnumfunc={novo_func.idfuncionario}")
            else:
                print(f"Funcionário já existe: idfuncionario={funcionario_exists.idfuncionario}")
        else:
            print("Utilizador 'enf.ana' não encontrado!")

        # 5. CRIAR MÉDICO PARA TESTE
        print("\n--- A CRIAR MÉDICO ---")
        
        user_med = db.query(models.Utilizador).filter(models.Utilizador.username == "dr.silva").first()
        
        if user_med:
            funcionario_med_exists = db.query(models.Funcionario).filter(
                models.Funcionario.idutilizador == user_med.idutilizador
            ).first()
            
            if not funcionario_med_exists:
                novo_func_med = models.Funcionario(
                    nome="Carlos",
                    apelido="Silva",
                    sexo="M",
                    nomehosp="Hospital PRODIGI Central",
                    idutilizador=user_med.idutilizador
                )
                db.add(novo_func_med)
                db.commit()
                db.refresh(novo_func_med)
                
                novo_med = models.Medico(
                    mednumfunc=novo_func_med.idfuncionario,
                    especialidade="Medicina Interna",
                    estagiario=False
                )
                db.add(novo_med)
                db.commit()
                print(f"Médico criado com mednumfunc={novo_func_med.idfuncionario}")
            else:
                print(f"Médico já existe: idfuncionario={funcionario_med_exists.idfuncionario}")
        else:
            print("Utilizador 'dr.silva' não encontrado!")



        # 6. INJETAR EPISÓDIOS SINTÉTICOS PARA TREINO DA IA
        print("\n--- A INJETAR DADOS SINTÉTICOS PARA TREINO DA IA ---")
        
        # Verificar se já existem episódios suficientes (mais de 50)
        episodios_existentes = db.query(models.Episodio).count()
        
        if episodios_existentes > 50:
            print(f"Já existem {episodios_existentes} episódios. A saltar injeção sintética.")
        else:
            # Obter referências necessárias
            hospital = db.query(models.Hospital).first()
            utentes = db.query(models.Utente).all()
            enfermeiro = db.query(models.Enfermeiro).first()
            medico = db.query(models.Medico).first()
            
            if not hospital or len(utentes) < 2 or not enfermeiro or not medico:
                print("⚠️ Dados base insuficientes para criar episódios sintéticos.")
            else:
                               
                # Prioridades Manchester
                prioridades = [
                    {"id": 1, "nome": "Imediata", "tempo_base": 0, "peso": 0.05},
                    {"id": 2, "nome": "Muito Urgente", "tempo_base": 15, "peso": 0.10},
                    {"id": 3, "nome": "Urgente", "tempo_base": 30, "peso": 0.35},
                    {"id": 4, "nome": "Pouco Urgente", "tempo_base": 60, "peso": 0.35},
                    {"id": 5, "nome": "Não Urgente", "tempo_base": 120, "peso": 0.15}
                ]
                
                horas_ponta = [9, 10, 11, 14, 15, 16, 20, 21, 22]
                horas_normais = [8, 12, 13, 17, 18, 19, 23]
                horas_mortas = [0, 1, 2, 3, 4, 5, 6, 7]
                
                num_sinteticos = 80
                novos_episodios = 0
                
                for i in range(num_sinteticos):
                    # Escolher prioridade (com pesos)
                    prioridade = random.choices(
                        prioridades,
                        weights=[p["peso"] for p in prioridades],
                        k=1
                    )[0]
                    
                    dias_atras = random.randint(1, 60)
                    dia_semana = random.randint(0, 6)
                    
                    rand_hora = random.random()
                    if rand_hora < 0.5:
                        hora = random.choice(horas_ponta)
                    elif rand_hora < 0.8:
                        hora = random.choice(horas_normais)
                    else:
                        hora = random.choice(horas_mortas)
                    
                    data_inicio = datetime.now() - timedelta(
                        days=dias_atras,
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                    data_inicio = data_inicio.replace(hour=hora, minute=random.randint(0, 59))
                    
                    tempo_base = prioridade["tempo_base"]
                    
                    if hora in horas_ponta:
                        ajuste = random.randint(10, 30)
                    elif hora in horas_normais:
                        ajuste = random.randint(0, 15)
                    else:
                        ajuste = random.randint(-10, 5)
                    
                    if dia_semana in [5, 6]:
                        ajuste += random.randint(-15, 0)
                    else:
                        ajuste += random.randint(0, 15)
                    
                    tempo_espera = max(5, tempo_base + ajuste + random.randint(-5, 15))
                    data_saida = data_inicio + timedelta(minutes=tempo_espera)
                    
                    utente = random.choice(utentes)
                    
                    novo_episodio = models.Episodio(
                        nomehosp=hospital.nomehosp,
                        numutente=utente.numutente,
                        idestadoatual=5,
                        datahorainicio=data_inicio,
                        datahorasaida=data_saida
                    )
                    db.add(novo_episodio)
                    db.flush()
                    
                    nova_triagem = models.Triagem(
                        numepis=novo_episodio.numepis,
                        enfnumfunc=enfermeiro.enfnumfunc,
                        idprioridade_cor=prioridade["id"],
                        sintomas=f"Dados sintéticos para treino IA #{i+1}",
                        tensaoarterial=f"{random.randint(100, 140)}/{random.randint(60, 90)}",
                        temperatura=round(random.uniform(36.0, 39.5), 1)
                    )
                    db.add(nova_triagem)
                    
                    novos_episodios += 1
                    
                    if novos_episodios % 20 == 0:
                        db.commit()
                        print(f"   {novos_episodios}/{num_sinteticos} episódios sintéticos criados...")
                
                db.commit()
                print(f"✅ {novos_episodios} episódios sintéticos injetados com sucesso!")
                print("   Agora podes treinar o modelo de IA em /ia/treinar")

        # 7. INJETAR EPISÓDIOS COM FLUXO COMPLETO
        print("\n--- A INJETAR EPISÓDIOS COM FLUXO COMPLETO ---")

        hospital = db.query(models.Hospital).first()
        utentes = db.query(models.Utente).all()
        enfermeiro = db.query(models.Enfermeiro).first()
        medico = db.query(models.Medico).first()
        tipos_ato = db.query(models.TipoAto).all()

        if not hospital or not utentes or not enfermeiro or not medico:
            print("⚠️ Dados base insuficientes.")
        else:
            sintomas_lista = [
                "Dor abdominal intensa", "Febre alta (39.5ºC)", "Dificuldade respiratória",
                "Traumatismo craniano", "Dor no peito", "Vómitos persistentes",
                "Tontura e desequilíbrio", "Dor lombar aguda", "Alergia grave",
                "Crise de asma", "Fratura suspeita no braço", "Corte profundo na mão"
            ]
            medicamentos = [
                ("Paracetamol", "500mg", "3x/dia", "5 dias"),
                ("Ibuprofeno", "400mg", "2x/dia", "7 dias"),
                ("Amoxicilina", "875mg", "2x/dia", "10 dias"),
                ("Omeprazol", "20mg", "1x/dia", "30 dias"),
                ("Metoclopramida", "10mg", "3x/dia", "3 dias"),
            ]

            # Distribuição das 60 por fase
            fases = (
                [1] * 10 +   # só admitidos
                [2] * 15 +   # admitidos + triagem
                [3] * 15 +   # + ato médico
                [4] * 10 +   # + internamento
                [5] * 10     # alta completa
            )
            random.shuffle(fases)

            criados = 0
            for fase in fases:
                utente = random.choice(utentes)
                dias_atras = random.randint(0, 30)
                hora = random.randint(7, 22)
                data_entrada = datetime.now() - timedelta(
                    days=dias_atras, hours=random.randint(0, 5),
                    minutes=random.randint(0, 59)
                )
                data_entrada = data_entrada.replace(hour=hora)

                # Criar episódio
                episodio = models.Episodio(
                    nomehosp=hospital.nomehosp,
                    numutente=utente.numutente,
                    idestadoatual=fase,
                    datahorainicio=data_entrada,
                    datahorasaida=data_entrada + timedelta(hours=random.randint(1, 8)) if fase == 5 else None
                )
                db.add(episodio)
                db.flush()

                prioridade = random.randint(1, 5)

                if fase >= 2:
                    triagem = models.Triagem(
                        numepis=episodio.numepis,
                        enfnumfunc=enfermeiro.enfnumfunc,
                        idprioridade_cor=prioridade,
                        sintomas=random.choice(sintomas_lista),
                        tensaoarterial=f"{random.randint(100,140)}/{random.randint(60,90)}",
                        temperatura=round(random.uniform(36.0, 39.5), 1)
                    )
                    db.add(triagem)

                if fase >= 3:
                    tipo_ato = random.choice(tipos_ato)
                    ato = models.Ato(
                        numepis=episodio.numepis,
                        mednumfunc=medico.mednumfunc,
                        idtipoato=tipo_ato.idtipoato,
                        datahorainic=data_entrada + timedelta(minutes=random.randint(30, 90)),
                        datahorafim=data_entrada + timedelta(minutes=random.randint(90, 180))
                    )
                    db.add(ato)
                    med = random.choice(medicamentos)
                    prescricao = models.Prescricao(
                        numepis=episodio.numepis,
                        mednumfunc=medico.mednumfunc,
                        medicamento=med[0], dosagem=med[1],
                        frequencia=med[2], duracao=med[3]
                    )
                    db.add(prescricao)

                if fase >= 4:
                    internamento = models.Internamento(
                        numepis=episodio.numepis,
                        cama_quarto=f"{random.randint(1,5)}{random.choice(['A','B','C'])}",
                        servico=random.choice(["Medicina Interna", "Cirurgia", "Ortopedia", "Cardiologia"]),
                        datahorainicio=data_entrada + timedelta(hours=random.randint(2, 6))
                    )
                    db.add(internamento)

                criados += 1
                if criados % 20 == 0:
                    db.commit()
                    print(f"   {criados}/60 episódios criados...")

            db.commit()
            print(f"✅ {criados} episódios com fluxo completo criados!")

        print("\n====== POVOAMENTO CONCLUÍDO COM SUCESSO ======")

    except Exception as e:
        db.rollback()
        print(f"Erro durante o povoamento: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    povoar_sistema()

