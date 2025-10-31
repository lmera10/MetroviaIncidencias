from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import uuid
import shutil

from app.models.database import Database, IncidenciaOperativa
from app.services.excel_parser import ExcelParser

router = APIRouter(prefix="/upload", tags=["upload"])
db = Database()
parser = ExcelParser()

def get_db():
    database = db.get_session()
    try:
        yield database
    finally:
        database.close()

@router.post("/")
async def upload_incidencias(file: UploadFile = File(...), db_session: Session = Depends(get_db)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos Excel")
    
    # Crear directorio de uploads si no existe
    os.makedirs("uploads", exist_ok=True)
    
    # Guardar archivo temporalmente
    file_path = f"uploads/temp_{uuid.uuid4()}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Parsear y procesar datos
        datos = parser.parse_excel(file_path)
        
        # Guardar en base de datos
        for dato in datos:
            incidencia = IncidenciaOperativa(**dato)
            db_session.add(incidencia)
        
        db_session.commit()
        
        return {
            "message": f"Se importaron {len(datos)} incidencias correctamente",
            "incidencias_importadas": len(datos)
        }
    
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
    
    finally:
        # Limpiar archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)