from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt  # <--- direto, sem passlib
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
import models
import schemas
from database import get_db

# ==============================================
# CONFIGURAÇÕES JWT
# ==============================================
SECRET_KEY = os.getenv("SECRET_KEY", "chave-local-desenvolvimento-nao-usar-em-producao")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas

# ==============================================
# HASH DE PASSWORDS (bcrypt direto)
# ==============================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a password em texto plano corresponde ao hash"""
    # Converter strings para bytes
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def get_password_hash(password: str) -> str:
    """Gera hash bcrypt de uma password"""
    # Limitar a 72 bytes (limite do bcrypt)
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

# ==============================================
# CRIAÇÃO E VALIDAÇÃO DE TOKENS JWT
# ==============================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT com expiração"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Decodifica e valida um token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ==============================================
# DEPENDÊNCIA: OBTER UTILIZADOR ATUAL (por token)
# ==============================================
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> models.Utilizador:
    """Obtém o utilizador autenticado a partir do token JWT"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(models.Utilizador).filter(models.Utilizador.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizador não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

# ==============================================
# DEPENDÊNCIAS PARA PERFIS (RBAC)
# ==============================================
def get_current_medico(current_user: models.Utilizador = Depends(get_current_user)) -> models.Utilizador:
    """Verifica se o utilizador atual é Médico (idperfil = 1)"""
    if current_user.idperfil != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a Médicos"
        )
    return current_user

def get_current_enfermeiro(current_user: models.Utilizador = Depends(get_current_user)) -> models.Utilizador:
    """Verifica se o utilizador atual é Enfermeiro (idperfil = 2)"""
    if current_user.idperfil != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a Enfermeiros"
        )
    return current_user

def get_current_rececionista(current_user: models.Utilizador = Depends(get_current_user)) -> models.Utilizador:
    """Verifica se o utilizador atual é Rececionista (idperfil = 3)"""
    if current_user.idperfil != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a Rececionistas"
        )
    return current_user

def get_current_admin(current_user: models.Utilizador = Depends(get_current_user)) -> models.Utilizador:
    """Verifica se o utilizador atual é Administrador (idperfil = 4)"""
    if current_user.idperfil != 4:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a Administradores"
        )
    return current_user

def get_current_rececionista_ou_admin(current_user: models.Utilizador = Depends(get_current_user)) -> models.Utilizador:
    """Permite acesso a Rececionistas (3) e Administradores (4)"""
    if current_user.idperfil not in [3, 4]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a Rececionistas e Administradores"
        )
    return current_user


