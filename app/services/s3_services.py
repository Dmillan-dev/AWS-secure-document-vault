import boto3
from botocore.exceptions import ClientError
import uuid
from app.core.config import settings
# Este servicio se encarga de manejar la interacción con Amazon S3 para subir archivos.
class S3Service:
    def __init__(self):
        # Inicializa el cliente de S3 usando las credenciales de la configuración
        # En un entorno real, estas credenciales deben manejarse con cuidado (ej. usando IAM roles, AWS Secrets Manager, etc.)
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_BUCKET_NAME

    def upload_file(self, file_content: bytes, original_filename: str, user_id: int) -> str:
        """
        Sube un archivo a S3 y devuelve la clave (s3_key) generada.
        """
        # Generamos un nombre único para evitar colisiones (ej. si dos usuarios suben "foto.png")
        # Estructuramos carpetas por usuario en S3: "user_1/1234-uuid-foto.png"
        # Extraemos la extensión del archivo para mantenerla en el nombre final
        file_extension = original_filename.split(".")[-1] if "." in original_filename else ""
        unique_id = str(uuid.uuid4())
        s3_key = f"user_{user_id}/{unique_id}.{file_extension}"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content
            )
            return s3_key
        except ClientError as e:
            print(f"Error subiendo archivo a S3: {e}")
            raise Exception("No se pudo subir el archivo al almacenamiento en la nube.")

# Instancia global del servicio para ser usada en los endpoints
# Esto permite reutilizar la conexión a S3 y mantener el código organizado.
# En un entorno real, podríamos considerar manejar esta instancia con un patrón de diseño más robusto o usar inyección de dependencias.
s3_service = S3Service()