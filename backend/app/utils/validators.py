import re
from datetime import datetime
from typing import Optional

def validar_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validar_fecha(fecha_str: str) -> bool:
    """Valida formato de fecha YYYY-MM-DD"""
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validar_hora(hora_str: str) -> bool:
    """Valida formato de hora HH:MM:SS"""
    try:
        datetime.strptime(hora_str, '%H:%M:%S')
        return True
    except ValueError:
        return False