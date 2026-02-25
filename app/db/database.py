import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Por defecto, intenta leer la variable de entorno, si no usa una local de prueba
# En producción, esta variable debe estar configurada con la URL de la base de datos real (RDS o Aurora)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vault_user:vault_pass@localhost:5432/vault_db")

# Configuración de SQLAlchemy para conectarse a la base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la base de datos en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()