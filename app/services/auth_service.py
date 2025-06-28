"""
Servicio de autenticación
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import logging

from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse, TokenData
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token
from app.core.exceptions import UnauthorizedException, ValidationException
from app.core.config import settings

logger = logging.getLogger(__name__)

class AuthService:
    """Servicio de autenticación"""
    
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
    
    async def authenticate_user(self, login_data: LoginRequest) -> TokenResponse:
        """Autenticar usuario y generar tokens"""
        
        # Buscar usuario por email
        db_user = await self.repository.get_by_email(login_data.email)
        
        if not db_user:
            raise UnauthorizedException("Credenciales inválidas")
        
        # Verificar contraseña
        if not verify_password(login_data.password, db_user.hashed_password):
            raise UnauthorizedException("Credenciales inválidas")
        
        # Verificar que el usuario esté activo
        if not db_user.is_active:
            raise UnauthorizedException("Cuenta desactivada")
        
        # Actualizar último login
        db_user.last_login = datetime.utcnow()
        await self.repository.db.commit()
        
        # Crear tokens
        token_data = {
            "user_id": db_user.id,
            "email": db_user.email,
            "username": db_user.username
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        logger.info(f"Usuario autenticado: {db_user.email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Renovar token de acceso usando refresh token"""
        
        # Verificar refresh token
        try:
            payload = verify_token(refresh_token, "refresh")
        except Exception:
            raise UnauthorizedException("Refresh token inválido")
        
        # Obtener usuario
        user_id = payload.get("user_id")
        db_user = await self.repository.get_by_id(user_id)
        
        if not db_user or not db_user.is_active:
            raise UnauthorizedException("Usuario no válido")
        
        # Crear nuevos tokens
        token_data = {
            "user_id": db_user.id,
            "email": db_user.email,
            "username": db_user.username
        }
        
        access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        logger.info(f"Token renovado para usuario: {db_user.email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def get_current_user(self, token: str) -> TokenData:
        """Obtener usuario actual desde token"""
        
        try:
            payload = verify_token(token, "access")
        except Exception:
            raise UnauthorizedException("Token inválido")
        
        # Verificar que el usuario existe y está activo
        user_id = payload.get("user_id")
        db_user = await self.repository.get_by_id(user_id)
        
        if not db_user or not db_user.is_active:
            raise UnauthorizedException("Usuario no válido")
        
        return TokenData(
            user_id=db_user.id,
            email=db_user.email,
            username=db_user.username
        )
