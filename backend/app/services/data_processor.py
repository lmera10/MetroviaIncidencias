import pandas as pd
from datetime import datetime, time
from typing import Dict, Any

class DataProcessor:
    def __init__(self):
        self.empresas_mapping = {
            'lmera@consorciostg.com.ec': 'STG',
            'mlopez@consorciostg.com.ec': 'STG',
            'jmoran@consorciostg.com.ec': 'STG',
            'mleon@consorciostg.com.ec': 'STG',
            'jmadero@consorciostg.com.ec': 'STG',
            'jpaz@consorciostg.com.ec': 'STG'
        }
        
        # Lista de columnas que pueden contener tiempo
        self.columnas_tiempo = [
            'Hora_programada', 'Hora_real', 'Ciclo', 'Hora_de_incidencia'
        ]
    
    def determinar_tipo_dia(self, fecha: datetime) -> str:
        """Determina si es día laboral, fin de semana o festivo"""
        if fecha.weekday() >= 5:  # 5=Sábado, 6=Domingo
            return 'Fin de semana'
        return 'Laboral'
    
    def determinar_turno(self, hora_str: str) -> str:
        """Determina el turno basado en la hora"""
        if not hora_str or pd.isna(hora_str) or hora_str == '' or hora_str is None:
            return 'No definido'
        
        try:
            # Si ya es un string en formato HH:MM:SS
            if isinstance(hora_str, str):
                hora_part = hora_str.split(' ')[0]  # Por si viene con fecha
                return self._clasificar_turno_desde_string(hora_part)
            # Si es datetime.time
            elif isinstance(hora_str, time):
                return self._clasificar_turno_desde_time(hora_str)
            else:
                return 'No definido'
        except:
            return 'No definido'
    
    def _clasificar_turno_desde_string(self, hora_str: str) -> str:
        """Clasifica turno desde string HH:MM:SS"""
        try:
            hora = datetime.strptime(hora_str, '%H:%M:%S').time()
            return self._clasificar_turno_desde_time(hora)
        except:
            try:
                # Intentar con formato HH:MM
                hora = datetime.strptime(hora_str, '%H:%M').time()
                return self._clasificar_turno_desde_time(hora)
            except:
                return 'No definido'
    
    def _clasificar_turno_desde_time(self, hora: time) -> str:
        """Clasifica turno desde objeto time"""
        if hora < datetime.strptime('12:00:00', '%H:%M:%S').time():
            return 'Mañana'
        elif hora < datetime.strptime('18:00:00', '%H:%M:%S').time():
            return 'Tarde'
        else:
            return 'Noche'
    
    def extraer_empresa(self, operador_email: str) -> str:
        """Extrae la empresa del email del operador"""
        if pd.isna(operador_email) or not operador_email:
            return 'Desconocida'
        return self.empresas_mapping.get(operador_email, 'Desconocida')
    
    def convertir_tiempo_a_string(self, tiempo_valor) -> str:
        """Convierte cualquier formato de tiempo a string HH:MM:SS"""
        if pd.isna(tiempo_valor) or tiempo_valor is None:
            return None
        
        # Si ya es string, devolver tal cual
        if isinstance(tiempo_valor, str):
            return tiempo_valor
        
        # Si es datetime.time
        if isinstance(tiempo_valor, time):
            return tiempo_valor.strftime('%H:%M:%S')
        
        # Si es timedelta (duración)
        if hasattr(tiempo_valor, 'total_seconds'):
            # Convertir timedelta a string HH:MM:SS
            total_segundos = int(tiempo_valor.total_seconds())
            horas = total_segundos // 3600
            minutos = (total_segundos % 3600) // 60
            segundos = total_segundos % 60
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        
        # Si es pandas Timestamp
        if hasattr(tiempo_valor, 'strftime'):
            try:
                return tiempo_valor.strftime('%H:%M:%S')
            except:
                pass
        
        # Si es float (duración en horas/decimal)
        if isinstance(tiempo_valor, float):
            try:
                horas = int(tiempo_valor)
                minutos = int((tiempo_valor - horas) * 60)
                return f"{horas:02d}:{minutos:02d}:00"
            except:
                pass
        
        # Si es otro tipo, convertir a string
        return str(tiempo_valor)
    
    def limpiar_datos(self, fila: Dict[str, Any]) -> Dict[str, Any]:
        """Limpia y normaliza los datos del Excel"""
        datos_limpios = {}
        
        for key, value in fila.items():
            if pd.isna(value):
                datos_limpios[key] = None
            else:
                # Convertir TODAS las columnas de tiempo a string
                if key in self.columnas_tiempo:
                    datos_limpios[key] = self.convertir_tiempo_a_string(value)
                else:
                    datos_limpios[key] = value
        
        return datos_limpios
    
    def procesar_fila(self, fila: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa una fila individual del Excel"""
        # Primero limpiar los datos
        fila_limpia = self.limpiar_datos(fila)
        
        # Procesar fecha
        fecha = fila_limpia.get('Fecha')
        fecha_obj = None
        
        if isinstance(fecha, str):
            try:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            except:
                try:
                    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
                except:
                    fecha_obj = None
        elif hasattr(fecha, 'to_pydatetime'):
            # Si es Timestamp de pandas
            fecha_obj = fecha.to_pydatetime()
        elif isinstance(fecha, datetime):
            fecha_obj = fecha
        
        resultado = fila_limpia.copy()
        
        # Asegurar que Fecha sea datetime
        resultado['Fecha'] = fecha_obj
        
        # Agregar campos derivados
        if fecha_obj:
            resultado['tipo_dia'] = self.determinar_tipo_dia(fecha_obj)
        else:
            resultado['tipo_dia'] = 'No definido'
            
        resultado['turno'] = self.determinar_turno(fila_limpia.get('Hora_programada', ''))
        resultado['empresa'] = self.extraer_empresa(fila_limpia.get('Operador', ''))
        
        return resultado