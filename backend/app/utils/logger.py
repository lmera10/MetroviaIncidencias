import logging
import sys
from datetime import datetime
import os

def setup_logger():
    """Configura el sistema de logging"""
    
    # Crear directorio de logs si no existe
    os.makedirs("logs", exist_ok=True)
    
    # Configurar formato
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configurar logging a archivo
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)