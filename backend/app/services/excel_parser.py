import pandas as pd
from typing import List, Dict, Any
from .data_processor import DataProcessor

class ExcelParser:
    def __init__(self):
        self.processor = DataProcessor()
    
    def mapear_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Mapea los nombres de columnas del Excel al formato de la base de datos"""
        mapeo_columnas = {
            'Fecha': 'Fecha',
            'Troncal': 'Troncal', 
            'Código de Ruta': 'Codigo_de_Ruta',
            'Ruta': 'Ruta',
            'Bus': 'Bus',
            'Bus de cambio': 'Bus_de_cambio',
            'Hora programada': 'Hora_programada',
            'Hora real': 'Hora_real', 
            'Ciclo': 'Ciclo',
            'Hora de incidencia': 'Hora_de_incidencia',
            'Parada': 'Parada',
            'Incidencia primaria': 'Incidencia_primaria',
            'Incidencia secundaria': 'Incidencia_secundaria',
            'Código de conductor': 'Codigo_de_conductor',
            'Conductor': 'Conductor',
            'Operador': 'Operador',
            'Observaciones': 'Observaciones'
        }
        
        # Renombrar columnas
        df_renombrado = df.rename(columns=mapeo_columnas)
        
        # Mantener solo las columnas que necesitamos
        columnas_necesarias = list(mapeo_columnas.values())
        columnas_existentes = [col for col in columnas_necesarias if col in df_renombrado.columns]
        
        return df_renombrado[columnas_existentes]
    
    def parse_excel(self, file_path: str) -> List[Dict[str, Any]]:
        """Parsea el archivo Excel y devuelve los datos procesados"""
        try:
            print(f"=== INICIANDO PROCESAMIENTO DE ARCHIVO ===")
            print(f"Archivo: {file_path}")
            
            # Leer el archivo Excel
            df = pd.read_excel(file_path)
            print(f"✅ Archivo leído. Columnas originales: {list(df.columns)}")
            print(f"📊 Total de filas: {len(df)}")
            
            # Mapear columnas
            df = self.mapear_columnas(df)
            print(f"✅ Columnas mapeadas: {list(df.columns)}")
            
            # Mostrar tipos de datos de las primeras filas
            print(f"📋 Tipos de datos de las primeras filas:")
            for i, (_, fila) in enumerate(df.head(3).iterrows()):
                print(f"  Fila {i}:")
                for col, val in fila.items():
                    print(f"    {col}: {val} (tipo: {type(val)})")
            
            # Convertir a lista de diccionarios
            datos = df.to_dict('records')
            
            # Procesar cada fila
            datos_procesados = []
            errores = 0
            
            for i, fila in enumerate(datos):
                try:
                    fila_procesada = self.processor.procesar_fila(fila)
                    datos_procesados.append(fila_procesada)
                    
                    # Mostrar detalles de las primeras 3 filas procesadas
                    if i < 3:
                        print(f"✅ Fila {i} procesada exitosamente:")
                        for key, value in fila_procesada.items():
                            print(f"   {key}: {value} (tipo: {type(value)})")
                            
                except Exception as e:
                    errores += 1
                    print(f"❌ Error procesando fila {i}: {e}")
                    print(f"   Datos de la fila problemática: {fila}")
                    continue
            
            print(f"=== PROCESAMIENTO COMPLETADO ===")
            print(f"✅ {len(datos_procesados)} filas procesadas exitosamente")
            print(f"❌ {errores} errores")
            
            return datos_procesados
        
        except Exception as e:
            print(f"❌ ERROR GENERAL AL PARSEAR: {e}")
            raise Exception(f"Error al parsear el archivo Excel: {str(e)}")