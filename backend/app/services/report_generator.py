import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func, extract  # <-- AGREGAR ESTA IMPORTACIÓN
from typing import Dict, List
from datetime import datetime, timedelta

from app.models.database import IncidenciaOperativa

class ReportGenerator:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def generar_reporte_diario(self, fecha: str) -> Dict:
        """Genera reporte consolidado del día"""
        
        # Estadísticas básicas
        total_incidencias = self.db.query(IncidenciaOperativa).filter(
            func.date(IncidenciaOperativa.fecha) == fecha  # <-- Ahora func está definido
        ).count()
        
        # Por turno
        por_turno = self.db.query(
            IncidenciaOperativa.turno,
            func.count(IncidenciaOperativa.id).label('total')  # <-- Ahora func está definido
        ).filter(
            func.date(IncidenciaOperativa.fecha) == fecha
        ).group_by(IncidenciaOperativa.turno).all()
        
        # Por troncal
        por_troncal = self.db.query(
            IncidenciaOperativa.troncal,
            func.count(IncidenciaOperativa.id).label('total')  # <-- Ahora func está definido
        ).filter(
            func.date(IncidenciaOperativa.fecha) == fecha
        ).group_by(IncidenciaOperativa.troncal).all()
        
        # Por tipo de incidencia
        por_tipo = self.db.query(
            IncidenciaOperativa.incidencia_primaria,
            func.count(IncidenciaOperativa.id).label('total')  # <-- Ahora func está definido
        ).filter(
            func.date(IncidenciaOperativa.fecha) == fecha
        ).group_by(IncidenciaOperativa.incidencia_primaria).all()
        
        # Por empresa
        por_empresa = self.db.query(
            IncidenciaOperativa.empresa,
            func.count(IncidenciaOperativa.id).label('total')  # <-- Ahora func está definido
        ).filter(
            func.date(IncidenciaOperativa.fecha) == fecha
        ).group_by(IncidenciaOperativa.empresa).all()
        
        return {
            'fecha': fecha,
            'total_incidencias': total_incidencias,
            'por_turno': [{'turno': item.turno, 'total': item.total} for item in por_turno],
            'por_troncal': [{'troncal': item.troncal, 'total': item.total} for item in por_troncal],
            'por_tipo_incidencia': [{'tipo': item.incidencia_primaria, 'total': item.total} for item in por_tipo],
            'por_empresa': [{'empresa': item.empresa, 'total': item.total} for item in por_empresa]
        }
    
    def generar_tendencia_semanal(self, fecha_inicio: str) -> List[Dict]:
        """Genera tendencia de incidencias por semana"""
        tendencias = []
        
        for i in range(7):  # Últimos 7 días
            fecha = (datetime.strptime(fecha_inicio, '%Y-%m-%d') - timedelta(days=i)).strftime('%Y-%m-%d')
            
            total = self.db.query(IncidenciaOperativa).filter(
                func.date(IncidenciaOperativa.fecha) == fecha  # <-- Ahora func está definido
            ).count()
            
            tendencias.append({
                'fecha': fecha,
                'total_incidencias': total
            })
        
        return tendencias
    
    def generar_reporte_comparativo(self, fecha1: str, fecha2: str) -> Dict:
        """Compara incidencias entre dos fechas"""
        reporte1 = self.generar_reporte_diario(fecha1)
        reporte2 = self.generar_reporte_diario(fecha2)
        
        return {
            'fecha1': reporte1,
            'fecha2': reporte2,
            'comparacion': {
                'diferencia_total': reporte1['total_incidencias'] - reporte2['total_incidencias'],
                'variacion_porcentual': (
                    (reporte1['total_incidencias'] - reporte2['total_incidencias']) / 
                    reporte2['total_incidencias'] * 100
                ) if reporte2['total_incidencias'] > 0 else 0
            }
        }