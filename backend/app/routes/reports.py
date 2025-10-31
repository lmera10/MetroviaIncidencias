from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.database import Database, IncidenciaOperativa
from app.services.report_generator import ReportGenerator
from app.models.schemas import EstadisticasResponse

router = APIRouter(prefix="/reports", tags=["reports"])
db = Database()

def get_db():
    database = db.get_session()
    try:
        yield database
    finally:
        database.close()

@router.get("/diario", response_model=EstadisticasResponse)
async def get_reporte_diario(
    fecha: str = Query(..., description="Fecha en formato YYYY-MM-DD"),
    db_session: Session = Depends(get_db)
):
    """Obtiene reporte consolidado del día"""
    try:
        generator = ReportGenerator(db_session)
        reporte = generator.generar_reporte_diario(fecha)
        
        return EstadisticasResponse(
            fecha=reporte['fecha'],
            total_incidencias=reporte['total_incidencias'],
            por_turno=reporte['por_turno'],
            por_troncal=reporte['por_troncal'],
            por_empresa=reporte.get('por_empresa', [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")

@router.get("/tendencia/semanal")
async def get_tendencia_semanal(
    fecha_fin: str = Query(None, description="Fecha final (YYYY-MM-DD)"),
    db_session: Session = Depends(get_db)
):
    """Obtiene tendencia de incidencias de la última semana"""
    if not fecha_fin:
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
    
    generator = ReportGenerator(db_session)
    tendencia = generator.generar_tendencia_semanal(fecha_fin)
    
    return {
        "periodo": "semanal",
        "fecha_fin": fecha_fin,
        "tendencia": tendencia
    }

@router.get("/comparativo")
async def get_reporte_comparativo(
    fecha1: str = Query(..., description="Primera fecha (YYYY-MM-DD)"),
    fecha2: str = Query(..., description="Segunda fecha (YYYY-MM-DD)"),
    db_session: Session = Depends(get_db)
):
    """Compara incidencias entre dos fechas"""
    generator = ReportGenerator(db_session)
    comparativo = generator.generar_reporte_comparativo(fecha1, fecha2)
    
    return comparativo

@router.get("/top-incidencias")
async def get_top_incidencias(
    limite: int = Query(10, description="Número de resultados"),
    db_session: Session = Depends(get_db)
):
    """Obtiene los tipos de incidencia más comunes"""
    resultados = db_session.query(
        IncidenciaOperativa.Incidencia_primaria,
        func.count(IncidenciaOperativa.id).label('total')
    ).group_by(
        IncidenciaOperativa.Incidencia_primaria
    ).order_by(
        func.count(IncidenciaOperativa.id).desc()
    ).limit(limite).all()
    
    return {
        "top_incidencias": [
            {"tipo": resultado.Incidencia_primaria, "total": resultado.total}
            for resultado in resultados
        ]
    }