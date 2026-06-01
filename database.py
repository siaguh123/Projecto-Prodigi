from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Esta URL liga o FastAPI ao contentor 'db' que viste no Podman
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user_admin:password123@hospital_db_container:5432/hospital_db")
#substituida pela |^| - O podman apontava para db e não db.container -> SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user_admin:password123@db:5432/hospital_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para as rotas usarem a BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        

        