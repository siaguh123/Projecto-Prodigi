from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# 1. Tabelas de Apoio (Lookup Tables)
class Hospital(Base):
    __tablename__ = "hospital"
    nomehosp = Column(String, primary_key=True)
    localizacao = Column(String)

class TipoAto(Base):
    __tablename__ = "tipoato"
    idtipoato = Column(Integer, primary_key=True, autoincrement=True)
    designacao = Column(String, unique=True)

# 2. Gestão de Utilizadores e Funcionários
class Utilizador(Base):
    __tablename__ = "utilizador"
    idutilizador = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    passwordhash = Column(String)
    idperfil = Column(Integer) # No teu SQL: 1-Médico, 2-Enfermeiro

class Funcionario(Base):
    __tablename__ = "funcionario"
    idfuncionario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    apelido = Column(String)
    sexo = Column(String)
    nomehosp = Column(String, ForeignKey("hospital.nomehosp"))
    idutilizador = Column(Integer, ForeignKey("utilizador.idutilizador"))

class Medico(Base):
    __tablename__ = "medico"
    mednumfunc = Column(Integer, ForeignKey("funcionario.idfuncionario"), primary_key=True)
    especialidade = Column(String)
    estagiario = Column(Boolean, default=False)

class Enfermeiro(Base):
    __tablename__ = "enfermeiro"
    enfnumfunc = Column(Integer, ForeignKey("funcionario.idfuncionario"), primary_key=True)
    grau = Column(String)

# 3. Núcleo do Hospital (Utentes e Urgências)
class Utente(Base):
    __tablename__ = "t1_utente"
    numutente = Column(Integer, primary_key=True)
    nome = Column(String)
    apelido = Column(String)
    localidade = Column(String)
    sexo = Column(String)
    datanasc = Column(Date)

class Episodio(Base):
    __tablename__ = "episodio"
    numepis = Column(Integer, primary_key=True)
    nomehosp = Column(String, ForeignKey("hospital.nomehosp"))
    numutente = Column(Integer, ForeignKey("t1_utente.numutente"))
    idestadoatual = Column(Integer)
    datahorainicio = Column(DateTime, default=datetime.utcnow)
    datahorasaida = Column(DateTime, nullable=True)

class Triagem(Base):
    __tablename__ = "triagem"
    numepis = Column(Integer, ForeignKey("episodio.numepis"), primary_key=True)
    enfnumfunc = Column(Integer, ForeignKey("enfermeiro.enfnumfunc"))
    idprioridade_cor = Column(Integer) # 1-Vermelho, 3-Amarelo, 4-Verde
    sintomas = Column(String)
    tensaoarterial = Column(String)
    temperatura = Column(Float)

# 4. Atos Médicos e Internamento
class Ato(Base):
    __tablename__ = "ato"
    idato = Column(Integer, primary_key=True, autoincrement=True)
    numepis = Column(Integer, ForeignKey("episodio.numepis"))
    mednumfunc = Column(Integer, ForeignKey("medico.mednumfunc"))
    idtipoato = Column(Integer, ForeignKey("tipoato.idtipoato"))
    datahorainic = Column(DateTime)
    datahorafim = Column(DateTime)

class Internamento(Base):
    __tablename__ = "internamento"
    numepis = Column(Integer, ForeignKey("episodio.numepis"), primary_key=True)
    cama_quarto = Column(String)
    servico = Column(String)
    datahorainicio = Column(DateTime, default=datetime.utcnow)

class Prescricao(Base):
    __tablename__ = "prescricao"
    idprescricao = Column(Integer, primary_key=True, autoincrement=True)
    numepis = Column(Integer, ForeignKey("episodio.numepis"))
    mednumfunc = Column(Integer, ForeignKey("medico.mednumfunc"))
    medicamento = Column(String)
    dosagem = Column(String)
    frequencia = Column(String)
    duracao = Column(String, nullable=True)
    datahoraprescricao = Column(DateTime, default=datetime.utcnow)
    