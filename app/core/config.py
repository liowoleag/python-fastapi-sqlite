"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Optional, Union
import os

class Settings(BaseSettings):
    # Project information
    PROJECT_NAME: str = "User Management Microservice"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Microservice for user management"
    
    # Environment configuration
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Database configuration
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./users.db",
        env="DATABASE_URL"
    )
    
    # Security configuration
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS configuration - FIXED
    ALLOWED_HOSTS: Union[str, List[str]] = Field(
        default="*",
        env="ALLOWED_HOSTS"
    )
    
    # Logging configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Pagination configuration
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v):
        """Parse ALLOWED_HOSTS from string or list"""
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            # If it's a comma-separated string
            return [host.strip() for host in v.split(",") if host.strip()]
        elif isinstance(v, list):
            return v
        else:
            return ["*"]  # Safe default value
    
    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, v):
        """Parse DEBUG from string"""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        # Avoid JSON parsing errors
        env_parse_none_str = None

# Global configuration instance
settings = Settings()
