from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.models.database import Database
from app.routes.upload import router as upload_router
from app.routes.queries import router as queries_router
from app.routes.reports import router as reports_router
from app.middleware.error_handler import global_error_handler
from app.utils.logger import setup_logger

# Configurar logging
logger = setup_logger()

# Inicializar base de datos
db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.create_tables()
    logger.info("Tablas de base de datos creadas/verificadas")
    logger.info("Aplicación iniciada correctamente")
    yield
    # Shutdown
    logger.info("Aplicación cerrada")

app = FastAPI(
    title="Sistema de Incidencias Operativas Metrovia",
    description="API para la gestión y consulta de incidencias operativas del Sistema Metrovia",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de manejo de errores
app.middleware("http")(global_error_handler)

# Incluir routers - VERIFICAR QUE ESTÉN ESTAS LÍNEAS
app.include_router(upload_router, prefix="/api/v1")
app.include_router(queries_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Sistema de Incidencias Operativas Metrovia"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)