from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class IncidenciaBase(BaseModel):
    fecha: datetime
    troncal: Optional[str] = None
    codigo_ruta: Optional[str] = None
    ruta: Optional[str] = None
    bus: Optional[str] = None
    bus_cambio: Optional[str] = None
    hora_programada: Optional[str] = None
    hora_real: Optional[str] = None
    ciclo: Optional[str] = None
    hora_incidencia: Optional[str] = None
    parada: Optional[str] = None
    incidencia_primaria: Optional[str] = None
    incidencia_secundaria: Optional[str] = None
    codigo_conductor: Optional[str] = None
    conductor: Optional[str] = None
    operador: Optional[str] = None
    observaciones: Optional[str] = None

class IncidenciaCreate(IncidenciaBase):
    pass

class IncidenciaResponse(IncidenciaBase):
    id: int
    tipo_dia: Optional[str] = None
    turno: Optional[str] = None
    empresa: Optional[str] = None
    
    class Config:
        from_attributes = True

class EstadisticasResponse(BaseModel):
    fecha: str
    total_incidencias: int
    por_turno: List[dict]
    por_troncal: List[dict]
    por_empresa: List[dict]

class FiltrosConsulta(BaseModel):
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    troncal: Optional[str] = None
    empresa: Optional[str] = None
    tipo_incidencia: Optional[str] = None
    turno: Optional[str] = None