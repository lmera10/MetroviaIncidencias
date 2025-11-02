import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Sistema de Incidencias Operativas Metrovia"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./incidencias.db")
    
    # File upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB

    EMPRESAS_MAPPING: dict = {
        'lmera@consorciostg.com.ec': 'STG',
        'mlopez@consorciostg.com.ec': 'STG',
        'jmoran@consorciostg.com.ec': 'STG',
        'mleon@consorciostg.com.ec': 'STG',
        'jmadero@consorciostg.com.ec': 'STG',
        'jpaz@consorciostg.com.ec': 'STG'
    }

settings = Settings()