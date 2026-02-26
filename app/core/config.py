import os
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env si existe
load_dotenv()
# En un entorno real, NUNCA debes tener un archivo .env con claves sensibles en tu repositorio.
# El archivo .env debe estar en tu .gitignore y las claves deben ser gestionadas de forma segura.
class Settings:
    PROJECT_NAME: str = "AWS Secure Document Vault"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "una-clave-secreta-muy-larga-y-compleja-para-desarrollo")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # --- NUEVO: Configuraciones de AWS ---
    # En un entorno real, estas claves NUNCA deben estar en el código.
    # Deben venir de las variables de entorno o de un servicio como AWS Secrets Manager.
    # Para generar estas claves, debes crear un usuario IAM en AWS con permisos adecuados y luego obtener sus credenciales.
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "eu-west-1") # Cambia esto por tu región
    AWS_BUCKET_NAME: str = os.getenv("AWS_BUCKET_NAME", "mi-bucket-document-vault-test")

settings = Settings()