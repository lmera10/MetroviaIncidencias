from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

Base = declarative_base()

class IncidenciaOperativa(Base):
    """Represents an operational incident."""
    __tablename__ = 'incidencias_operativas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    troncal = Column(String(10))
    codigo_de_ruta = Column(String(10))
    ruta = Column(String(255))
    bus = Column(String(20))
    bus_de_cambio = Column(String(20))
    hora_programada = Column(String(20))
    hora_real = Column(String(20))
    ciclo = Column(String(20))
    hora_de_incidencia = Column(String(20))
    parada = Column(String(255))
    incidencia_primaria = Column(String(255))
    incidencia_secundaria = Column(String(255))
    codigo_de_conductor = Column(String(20))
    conductor = Column(String(255))
    operador = Column(String(255))
    observaciones = Column(Text)
    
    # Derived fields for analysis
    tipo_dia = Column(String(20))  # Laboral, Fin de semana, Festivo
    turno = Column(String(20))     # Mañana, Tarde, Noche
    empresa = Column(String(100))  # Extracted from operator's email

class Database:
    """Handles database connections and sessions."""
    def __init__(self):
        """Initializes the database engine and session factory."""
        self.engine = create_engine(settings.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Creates all database tables."""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Returns a new database session."""
        return self.SessionLocal()