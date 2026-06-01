from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

# ----- CONFIGURAÇÃO GLOBAL -----
# model_config para permitir que o Pydantic leia modelos do SQLAlchemy
# -------------------------------

# ----- 1. Tabelas de Apoio (Lookup) -----
class HospitalBase(BaseModel):
    nomehosp: str
    localizacao: Optional[str] = None

class HospitalCreate(HospitalBase):
    pass

class Hospital(HospitalBase):
    model_config = ConfigDict(from_attributes=True)

class TipoAtoBase(BaseModel):
    idtipoato: Optional[int] = None
    designacao: str

class TipoAtoCreate(TipoAtoBase):
    pass

class TipoAto(TipoAtoBase):
    model_config = ConfigDict(from_attributes=True)

# ----- 2. Utilizadores e Funcionários -----
class UtilizadorBase(BaseModel):
    username: str
    idperfil: int  # 1-Médico, 2-Enfermeiro

class UtilizadorCreate(UtilizadorBase):
    password: str  # Recebemos a pass para fazer hash no backend

class UtilizadorOut(UtilizadorBase):
    idutilizador: int
    model_config = ConfigDict(from_attributes=True)

class FuncionarioBase(BaseModel):
    nome: str
    apelido: str
    sexo: str
    nomehosp: str
    idutilizador: int

class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    idfuncionario: int
    model_config = ConfigDict(from_attributes=True)

class NovoFuncionarioForm(BaseModel):
    username: str
    password: str
    idperfil: int
    nome: str
    apelido: str
    sexo: str
    nomehosp: str
    especialidade: Optional[str] = None
    grau: Optional[str] = None
    estagiario: bool = False

# ----- 3. Utentes e Urgências -----
class UtenteBase(BaseModel):
    numutente: int
    nome: str
    apelido: str
    localidade: Optional[str] = None
    sexo: str
    datanasc: date

class UtenteCreate(UtenteBase):
    pass

class Utente(UtenteBase):
    model_config = ConfigDict(from_attributes=True)

class EpisodioBase(BaseModel):
    nomehosp: str
    numutente: int
    idestadoatual: int  # Começa em 1 (Admitido)

class EpisodioCreate(EpisodioBase):
    # Quando criamos, enviamos apenas o hospital, o utente e o estado.
    # O Python e a BD tratam do ID e da Data sozinhos!
    pass

class Episodio(EpisodioBase):
    numepis: int        # Na resposta da API, o número já vai preenchido
    datahorainicio: datetime
    datahorasaida: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# ==============================================
# AUTENTICAÇÃO (JWT)
# ==============================================

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    idperfil: int
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None
    

# ==============================================
# TRIAGEM
# ==============================================

class TriagemBase(BaseModel):
    numepis: int
    enfnumfunc: int
    idprioridade_cor: int
    sintomas: Optional[str] = None
    tensaoarterial: Optional[str] = None
    temperatura: Optional[float] = None

class TriagemCreate(TriagemBase):
    pass

class TriagemOut(TriagemBase):
    model_config = ConfigDict(from_attributes=True)

class AtoBase(BaseModel):
    numepis: int
    mednumfunc: int
    idtipoato: int
    datahorainic: datetime
    datahorafim: Optional[datetime] = None

class AtoCreate(AtoBase):
    pass

class AtoOut(AtoBase):
    idato: int
    model_config = ConfigDict(from_attributes=True)

       # ==============================================
# INTERNAMENTO
# ==============================================

class InternamentoBase(BaseModel):
    numepis: int
    cama_quarto: str
    servico: str
    datahorainicio: Optional[datetime] = None

class InternamentoCreate(InternamentoBase):
    pass

class InternamentoOut(InternamentoBase):
    model_config = ConfigDict(from_attributes=True)

# ==============================================
# PRESCRIÇÕES
# ==============================================

class PrescricaoBase(BaseModel):
    numepis: int
    mednumfunc: int
    medicamento: str
    dosagem: str
    frequencia: str
    duracao: Optional[str] = None

class PrescricaoCreate(PrescricaoBase):
    pass

class PrescricaoOut(PrescricaoBase):
    idprescricao: int
    datahoraprescricao: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

