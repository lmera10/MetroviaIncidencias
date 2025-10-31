from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def global_error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as http_exc:
        # Manejar excepciones HTTP conocidas
        return JSONResponse(
            status_code=http_exc.status_code,
            content={"detail": http_exc.detail}
        )
    except Exception as exc:
        # Manejar excepciones inesperadas
        logger.error(f"Error inesperado: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"}
        )