"""
Router para health checks
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging
import os

from app.core.database import get_db
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    """
    Health check básico
    
    Retorna el estado básico de la aplicación
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": "SQLite"
    }

@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check detallado
    
    Incluye verificación de base de datos SQLite
    """
    health_status = {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": "SQLite",
        "checks": {}
    }
    
    # Verificar base de datos SQLite
    try:
        await db.execute(text("SELECT 1"))
        
        # Verificar si el archivo de base de datos existe
        db_file_exists = os.path.exists("./users.db")
        db_file_size = os.path.getsize("./users.db") if db_file_exists else 0
        
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "SQLite connection successful",
            "file_exists": db_file_exists,
            "file_size_bytes": db_file_size
        }
    except Exception as e:
        logger.error(f"SQLite health check failed: {e}")
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"SQLite connection failed: {str(e)}"
        }
    
    return health_status
