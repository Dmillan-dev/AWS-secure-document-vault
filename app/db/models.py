from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

# En esta fase inicial, definimos dos modelos básicos: User y Document.
# El modelo User representa a los usuarios que pueden autenticarse en la API,
# mientras que el modelo Document representa los archivos que los usuarios pueden subir y gestionar.

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relación: Un usuario puede tener muchos documentos
    documents = relationship("Document", back_populates="owner")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    s3_key = Column(String, unique=True, nullable=True) # Lo usaremos con AWS
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_encrypted = Column(Boolean, default=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="documents")