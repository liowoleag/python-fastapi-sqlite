"""
Database configuration with SQLAlchemy async - SQLite
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, text
import logging
import asyncio
import os
from typing import AsyncGenerator

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create directory for database if it doesn't exist
db_path = "./users.db"
db_dir = os.path.dirname(os.path.abspath(db_path))
if not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)
    logger.info(f"Directory created: {db_dir}")

# Create async engine for SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    # SQLite specific configurations
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base for models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

async def check_db_connection():
    """Check database connection"""
    try:
        # Try to create database file if it doesn't exist
        if not os.path.exists(db_path):
            logger.info(f"Creating database file: {db_path}")
            # Create empty file
            open(db_path, 'a').close()
        
        async with engine.begin() as conn:
            # Execute simple query with text()
            result = await conn.execute(text("SELECT 1 as test"))
            test_value = result.scalar()
            
        logger.info(f"SQLite connection established successfully. Test: {test_value}")
        return True
    except Exception as e:
        logger.error(f"Error connecting to SQLite: {e}")
        logger.error(f"DATABASE_URL: {settings.DATABASE_URL}")
        logger.error(f"DB file exists: {os.path.exists(db_path)}")
        logger.error(f"Directory permissions: {oct(os.stat(db_dir).st_mode)[-3:] if os.path.exists(db_dir) else 'N/A'}")
        return False

async def init_db():
    """Initialize database by creating all tables"""
    try:
        logger.info("Starting SQLite database creation...")
        
        # Import all models BEFORE creating tables
        from app.models.user import User
        logger.info("Models imported successfully")
        
        # Verify model is registered
        logger.info(f"Tables registered in metadata: {list(Base.metadata.tables.keys())}")
        
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            logger.info("CREATE TABLE command executed")
            
        # Verify tables were created successfully
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = result.fetchall()
            table_names = [table[0] for table in tables]
            logger.info(f"Tables created in SQLite: {table_names}")
            
            if 'users' not in table_names:
                logger.error("❌ 'users' table was not created successfully")
                raise Exception("'users' table was not created")
            else:
                logger.info("✅ 'users' table created successfully")
                
                # Verify users table structure
                result = await conn.execute(text("PRAGMA table_info(users)"))
                columns = result.fetchall()
                logger.info(f"Users table columns: {[col[1] for col in columns]}")
            
    except Exception as e:
        logger.error(f"Error initializing SQLite database: {e}")
        logger.error(f"Error type: {type(e)}")
        raise
