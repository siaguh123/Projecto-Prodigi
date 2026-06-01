from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime

# =====================================================================
# 1. FUNÇÕES PARA UTENTES (Admissão)
# =====================================================================
def get_utente(db: Session, numutente: int):
    return db.query(models.Utente).filter(models.Utente.numutente == numutente).first()

def create_utente(db: Session, utente: schemas.UtenteCreate):
    db_utente = models.Utente(**utente.model_dump())
    db.add(db_utente)
    db.commit()
    db.refresh(db_utente)
    return db_utente

# Adicionado para homogeneidade do código (Linha 72 do main.py)
def get_all_utentes(db: Session):
    return db.query(models.Utente).all()


# =====================================================================
# 2. FUNÇÕES PARA HOSPITAIS (Configuração)
# =====================================================================
def get_hospital(db: Session, nomehosp: str):
    return db.query(models.Hospital).filter(models.Hospital.nomehosp == nomehosp).first()

def create_hospital(db: Session, hospital: schemas.HospitalCreate):
    db_hospital = models.Hospital(**hospital.model_dump())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

# Adicionado para homogeneidade do código (Linha 89 do main.py)
def get_all_hospitais(db: Session):
    return db.query(models.Hospital).all()


# =====================================================================
# 3. FUNÇÕES PARA EPISÓDIOS (Bloco 2 - Urgências)
# =====================================================================
def criar_episodio(db: Session, episodio: schemas.EpisodioCreate):
    db_episodio = models.Episodio(**episodio.model_dump())
    db.add(db_episodio)
    db.commit()
    db.refresh(db_episodio)
    return db_episodio

def obter_episodios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Episodio).offset(skip).limit(limit).all()

def obter_episodio_por_id(db: Session, numepis: int):
    return db.query(models.Episodio).filter(models.Episodio.numepis == numepis).first()

# ==============================================
# 4. FUNÇÕES PARA TRIAGEM
# ==============================================

# ==============================================
# 4. FUNÇÕES PARA TRIAGEM
# ==============================================

def create_triagem(db: Session, triagem: schemas.TriagemCreate):
    """
    Regista uma nova triagem associada a um episódio.
    Apenas enfermeiros podem criar triagem.
    """
    # Verificar se o episódio existe
    episodio = db.query(models.Episodio).filter(models.Episodio.numepis == triagem.numepis).first()
    if not episodio:
        raise ValueError(f"Episódio {triagem.numepis} não encontrado")
    
    # Verificar se o enfermeiro existe
    enfermeiro = db.query(models.Enfermeiro).filter(models.Enfermeiro.enfnumfunc == triagem.enfnumfunc).first()
    if not enfermeiro:
        raise ValueError(f"Enfermeiro com id {triagem.enfnumfunc} não encontrado")
    
    # Verificar se já existe triagem para este episódio
    existe = db.query(models.Triagem).filter(models.Triagem.numepis == triagem.numepis).first()
    if existe:
        raise ValueError(f"Episódio {triagem.numepis} já possui triagem registada")
    
    db_triagem = models.Triagem(**triagem.model_dump())
    db.add(db_triagem)
    db.commit()
    db.refresh(db_triagem)
    return db_triagem

def get_triagem_by_episodio(db: Session, numepis: int):
    """Obtém a triagem de um episódio específico"""
    return db.query(models.Triagem).filter(models.Triagem.numepis == numepis).first()

def get_all_triagens(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as triagens"""
    return db.query(models.Triagem).offset(skip).limit(limit).all()

# ==============================================
# 5. FUNÇÕES PARA ATO MÉDICO
# ==============================================

def create_ato(db: Session, ato: schemas.AtoCreate):
    """
    Regista um novo ato médico associado a um episódio.
    Apenas médicos podem criar atos.
    """
    # Verificar se o episódio existe
    episodio = db.query(models.Episodio).filter(models.Episodio.numepis == ato.numepis).first()
    if not episodio:
        raise ValueError(f"Episódio {ato.numepis} não encontrado")
    
    # Verificar se o médico existe
    medico = db.query(models.Medico).filter(models.Medico.mednumfunc == ato.mednumfunc).first()
    if not medico:
        raise ValueError(f"Médico com id {ato.mednumfunc} não encontrado")
    
    # Verificar se o tipo de ato existe
    tipo_ato = db.query(models.TipoAto).filter(models.TipoAto.idtipoato == ato.idtipoato).first()
    if not tipo_ato:
        raise ValueError(f"Tipo de ato {ato.idtipoato} não encontrado")
    
    db_ato = models.Ato(**ato.model_dump())
    db.add(db_ato)
    db.commit()
    db.refresh(db_ato)
    return db_ato

def get_atos_by_episodio(db: Session, numepis: int):
    """Obtém todos os atos médicos de um episódio específico"""
    return db.query(models.Ato).filter(models.Ato.numepis == numepis).all()

def get_all_atos(db: Session, skip: int = 0, limit: int = 100):
    """Lista todos os atos médicos"""
    return db.query(models.Ato).offset(skip).limit(limit).all()

def get_ato_by_id(db: Session, idato: int):
    """Obtém um ato médico pelo ID"""
    return db.query(models.Ato).filter(models.Ato.idato == idato).first()

# ==============================================
# 6. FUNÇÕES PARA INTERNAMENTO
# ==============================================

def create_internamento(db: Session, internamento: schemas.InternamentoCreate):
    """
    Regista um novo internamento associado a um episódio.
    Apenas médicos podem criar internamentos.
    """
    # Verificar se o episódio existe
    episodio = db.query(models.Episodio).filter(models.Episodio.numepis == internamento.numepis).first()
    if not episodio:
        raise ValueError(f"Episódio {internamento.numepis} não encontrado")
    
    # Verificar se já existe internamento para este episódio
    existe = db.query(models.Internamento).filter(
        models.Internamento.numepis == internamento.numepis
    ).first()
    if existe:
        raise ValueError(f"Episódio {internamento.numepis} já possui internamento registado")
    
    # Se datahorainicio não foi fornecida, usar a data/hora atual
    if internamento.datahorainicio is None:
        internamento.datahorainicio = datetime.utcnow()
    
    db_internamento = models.Internamento(**internamento.model_dump())
    db.add(db_internamento)
    db.commit()
    db.refresh(db_internamento)
    
    # Atualizar o estado do episódio para "Internado" (estado 4)
    episodio.idestadoatual = 4
    db.commit()
    
    return db_internamento

def get_internamento_by_episodio(db: Session, numepis: int):
    """Obtém o internamento de um episódio específico"""
    return db.query(models.Internamento).filter(
        models.Internamento.numepis == numepis
    ).first()

def get_all_internamentos(db: Session, skip: int = 0, limit: int = 100):
    """Lista todos os internamentos"""
    return db.query(models.Internamento).offset(skip).limit(limit).all()

# ==============================================
# 7. FUNÇÃO PARA ENCERRAR EPISÓDIO (ALTA)
# ==============================================

# ==============================================
# 8. FUNÇÕES PARA PRESCRIÇÕES
# ==============================================

def create_prescricao(db: Session, prescricao: schemas.PrescricaoCreate):
    episodio = db.query(models.Episodio).filter(models.Episodio.numepis == prescricao.numepis).first()
    if not episodio:
        raise ValueError(f"Episódio {prescricao.numepis} não encontrado")
    medico = db.query(models.Medico).filter(models.Medico.mednumfunc == prescricao.mednumfunc).first()
    if not medico:
        raise ValueError(f"Médico {prescricao.mednumfunc} não encontrado")
    db_prescricao = models.Prescricao(**prescricao.model_dump())
    db.add(db_prescricao)
    db.commit()
    db.refresh(db_prescricao)
    return db_prescricao

def get_prescricoes_by_episodio(db: Session, numepis: int):
    return db.query(models.Prescricao).filter(models.Prescricao.numepis == numepis).all()

def get_all_prescricoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prescricao).offset(skip).limit(limit).all()

# ==============================================
# 7. FUNÇÃO PARA ENCERRAR EPISÓDIO (ALTA)
# ==============================================

def encerrar_episodio(db: Session, numepis: int):
    """
    Encerra um episódio de urgência (Alta Médica).
    
    - Atualiza datahorasaida para o momento atual
    - Altera idestadoatual para 5 (Alta)
    """
    from datetime import datetime
    
    # Verificar se o episódio existe
    episodio = db.query(models.Episodio).filter(models.Episodio.numepis == numepis).first()
    if not episodio:
        raise ValueError(f"Episódio {numepis} não encontrado")
    
    # Verificar se já está encerrado
    if episodio.idestadoatual == 5:
        raise ValueError(f"Episódio {numepis} já está encerrado (Alta)")
    
    # Verificar se tem data de saída (se não tiver, atribuir agora)
    if episodio.datahorasaida is None:
        episodio.datahorasaida = datetime.utcnow()
    
    # Atualizar estado para Alta (5)
    episodio.idestadoatual = 5
    
    db.commit()
    db.refresh(episodio)
    
    return episodio


