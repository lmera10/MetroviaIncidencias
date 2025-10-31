from .upload import router as upload_router
from .queries import router as queries_router
from .reports import router as reports_router

__all__ = ["upload_router", "queries_router", "reports_router"]