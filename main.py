"""
Main entry point for the FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import os
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db, check_db_connection
from app.core.exceptions import CustomException
from app.routers import users, auth, health
from app.core.logging_config import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting application with SQLite...")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"DATABASE_URL: {settings.DATABASE_URL}")
    
    try:
        # Check database connection with retries
        max_retries = 3
        connection_ok = False
        
        for attempt in range(max_retries):
            logger.info(f"Connection attempt {attempt + 1}/{max_retries}")
            
            if await check_db_connection():
                logger.info("Database connection established")
                connection_ok = True
                break
            else:
                if attempt < max_retries - 1:
                    logger.warning("Retrying connection in 2 seconds...")
                    import asyncio
                    await asyncio.sleep(2)
                else:
                    logger.error("Could not establish connection after all attempts")
        
        if not connection_ok:
            logger.warning("Continuing without database connection for debugging...")
        else:
            # Initialize database only if connection works
            logger.info("Initializing database...")
            await init_db()
            logger.info("SQLite database initialized successfully")
            
            # Additional verification
            try:
                from app.core.database import AsyncSessionLocal
                from sqlalchemy import text
                async with AsyncSessionLocal() as session:
                    result = await session.execute(text("SELECT COUNT(*) FROM users"))
                    count = result.scalar()
                    logger.info(f"Users in database: {count}")
            except Exception as e:
                logger.warning(f"Could not verify users: {e}")
        
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        logger.warning("Continuing with partial initialization...")
    
    yield
    
    logger.info("Shutting down application...")

# Create FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="User management microservice with FastAPI and SQLite",
    version=settings.VERSION,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Global exception handler
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred"
        }
    )

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "database": "SQLite",
        "docs": "/docs",
        "health": "/api/v1/health",
        "working_directory": os.getcwd(),
        "database_url": settings.DATABASE_URL
    }

@app.get("/debug")
async def debug_info():
    """Debug endpoint to check configuration"""
    return {
        "working_directory": os.getcwd(),
        "database_url": settings.DATABASE_URL,
        "database_file_exists": os.path.exists("./users.db"),
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "files_in_directory": os.listdir("."),
        "permissions": oct(os.stat(".").st_mode)[-3:] if os.path.exists(".") else "N/A"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )
