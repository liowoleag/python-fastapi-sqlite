"""
Router para autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.core.exceptions import UnauthorizedException

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Autenticar usuario y obtener tokens de acceso
    
    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    
    Retorna tokens de acceso y refresco
    """
    auth_service = AuthService(db)
    return await auth_service.authenticate_user(login_data)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Renovar token de acceso usando refresh token
    
    - **refresh_token**: Token de refresco válido
    
    Retorna nuevos tokens de acceso y refresco
    """
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(refresh_data.refresh_token)

@router.post("/logout")
async def logout():
    """
    Cerrar sesión (logout)
    
    En una implementación completa, aquí se invalidarían los tokens
    Por ahora, simplemente retorna un mensaje de éxito
    """
    return {"message": "Sesión cerrada exitosamente"}
