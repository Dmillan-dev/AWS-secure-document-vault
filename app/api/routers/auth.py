from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# En esta fase inicial, implementamos un sistema de autenticación simple usando JWT.
# Esto nos permitirá proteger ciertos endpoints y asegurarnos de que solo los usuarios autenticados puedan acceder
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import User

router = APIRouter()

# 1. Endpoint para crear un usuario de prueba (Borrar en producción)
# Este endpoint es solo para propósitos de prueba y desarrollo. En un entorno de producción, deberíamos implementar un sistema de registro más robusto y seguro.
@router.post("/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    
    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario creado exitosamente", "user": new_user.username}

# 2. Login usando la Base de Datos REAL
@router.post("/login", response_model=dict)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db) # <-- Inyectamos la BD
):
    # Buscar usuario en Postgres
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint protegido para verificar que la autenticación funciona
@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"message": "Si ves esto, estás autenticado", "user": current_user}