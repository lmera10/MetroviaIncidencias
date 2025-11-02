from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from django.http import JsonResponse
from app.models.database import Database, IncidenciaOperativa

router = APIRouter(prefix="/queries", tags=["queries"])
db = Database()

def test_endpoint(request):
    data = {
        "mensaje": "API funcionando correctamente"
    }
    return JsonResponse(data)

def get_db():
    database = db.get_session()
    try:
        yield database
    finally:
        database.close()

def formatear_incidencia(incidencia):
    """Formatea una incidencia para convertir datetime a string"""
    incidencia_dict = {}
    
    for column in incidencia.__table__.columns:
        value = getattr(incidencia, column.name)
        
        # Convertir datetime a string
        if isinstance(value, datetime):
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        
        incidencia_dict[column.name] = value
    
    return incidencia_dict

@router.get("/incidencias")
async def get_incidencias(
    fecha_inicio: str = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: str = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    troncal: str = Query(None),
    empresa: str = Query(None),
    tipo_incidencia: str = Query(None),
    db_session: Session = Depends(get_db)
):
    query = db_session.query(IncidenciaOperativa)
    
    # Filtros
    if fecha_inicio and fecha_fin:
        query = query.filter(
            IncidenciaOperativa.fecha.between(fecha_inicio, fecha_fin)
        )
    
    if troncal:
        query = query.filter(IncidenciaOperativa.troncal == troncal)
    
    if empresa:
        query = query.filter(IncidenciaOperativa.empresa == empresa)
    
    if tipo_incidencia:
        query = query.filter(IncidenciaOperativa.incidencia_primaria.contains(tipo_incidencia))
    
    resultados = query.all()
    
    # Convertir resultados a diccionarios formateados
    incidencias_dict = [formatear_incidencia(incidencia) for incidencia in resultados]
    
    return {"total": len(resultados), "incidencias": incidencias_dict}

@router.get("/estadisticas/diarias")
async def get_estadisticas_diarias(
    fecha: str = Query(..., description="Fecha (YYYY-MM-DD)"),
    db_session: Session = Depends(get_db)
):
    # Estadísticas por hora del día
    estadisticas = db_session.query(
        func.count(IncidenciaOperativa.id).label('total'),
        IncidenciaOperativa.turno
    ).filter(
        func.date(IncidenciaOperativa.fecha) == fecha
    ).group_by(IncidenciaOperativa.turno).all()
    
    return {
        "fecha": fecha,
        "estadisticas": [
            {"turno": stat.turno, "total": stat.total} for stat in estadisticas
        ]
    }

@router.get("/tendencias/mensuales")
async def get_tendencias_mensuales(
    año: int = Query(..., description="Año"),
    db_session: Session = Depends(get_db)
):
    tendencias = db_session.query(
        extract('month', IncidenciaOperativa.fecha).label('mes'),
        func.count(IncidenciaOperativa.id).label('total')
    ).filter(
        extract('year', IncidenciaOperativa.fecha) == año
    ).group_by('mes').order_by('mes').all()
    
    return {
        "año": año,
        "tendencias": [
            {"mes": int(tendencia.mes), "total": tendencia.total} for tendencia in tendencias
        ]
    }