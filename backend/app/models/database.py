from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# CORREGIR ESTA IMPORTACIÓN:
from app.config import settings  # En lugar de ..config

Base = declarative_base()

class IncidenciaOperativa(Base):
    __tablename__ = 'incidencias_operativas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Fecha = Column(DateTime, nullable=False)
    Troncal = Column(String(10))
    Codigo_de_Ruta = Column(String(10))
    Ruta = Column(String(255))
    Bus = Column(String(20))
    Bus_de_cambio = Column(String(20))
    Hora_programada = Column(String(20))
    Hora_real = Column(String(20))
    Ciclo = Column(String(20))
    Hora_de_incidencia = Column(String(20))
    Parada = Column(String(255))
    Incidencia_primaria = Column(String(255))
    Incidencia_secundaria = Column(String(255))
    Codigo_de_conductor = Column(String(20))
    Conductor = Column(String(255))
    Operador = Column(String(255))
    Observaciones = Column(Text)
    
    # Campos derivados para análisis
    tipo_dia = Column(String(20))  # Laboral, Fin de semana, Festivo
    turno = Column(String(20))     # Mañana, Tarde, Noche
    empresa = Column(String(100))  # Extraída del email del operador

class Database:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()