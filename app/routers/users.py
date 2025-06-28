"""
Router para gestión de usuarios
"""
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.services.user_service import UserService
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserList, PasswordChange
)
from app.schemas.auth import TokenData
from app.routers.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Crear un nuevo usuario
    
    - **email**: Email único del usuario
    - **username**: Nombre de usuario único
    - **first_name**: Nombre del usuario
    - **last_name**: Apellido del usuario
    - **password**: Contraseña (mínimo 8 caracteres, debe incluir mayúscula, minúscula y número)
    - **confirm_password**: Confirmación de contraseña
    - **phone**: Teléfono (opcional)
    - **bio**: Biografía (opcional)
    - **avatar_url**: URL del avatar (opcional)
    """
    user_service = UserService(db)
    return await user_service.create_user(user_data)

@router.get("/", response_model=UserList)
async def get_users(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(20, ge=1, le=100, description="Tamaño de página"),
    search: Optional[str] = Query(None, description="Buscar por nombre, email o username"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    current_user: TokenData = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener lista paginada de usuarios
    
    - **page**: Número de página (por defecto 1)
    - **size**: Tamaño de página (por defecto 20, máximo 100)
    - **search**: Buscar en nombre, email o username
    - **is_active**: Filtrar por usuarios activos/inactivos
    
    Requiere autenticación
    """
    user_service = UserService(db)
    return await user_service.get_users(
        page=page,
        size=size,
        search=search,
        is_active=is_active
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: TokenData = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener perfil del usuario actual
    
    Requiere autenticación
    """
    user_service = UserService(db)
    return await user_service.get_user_by_id(current_user.user_id)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int = Path(..., description="ID del usuario"),
    current_user: TokenData = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener usuario por ID
    
    - **user_id**: ID del usuario a obtener
    
    Requiere autenticación
    """
    user_service = UserService(db)
    return await user_service.get_user_by_id(user_id)

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: TokenData = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar perfil del usuario actual
    
    - **first_name**: Nombre (opcional)
    - **last_name**: Apellido (opcional)
    - **phone**: Teléfono (opcional)
    - **bio**: Biografía (opcional)
    - **avatar_url**: URL del avatar (opcional)
    
    Requiere autenticación
    """
    user_service = UserService(db)
    return await user_service.update_user(current_user.user_id, user_data)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_data: UserUpdate,
    user_id: int = Path(..., description="ID del usuario"),
    current_user: TokenData = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar usuario por ID
    
    - **user_id**: ID del usuario a actualizar
    - **first_name**: Nombre (opcional)
    - **last_name**: Apellido (opcional)
    - **phone**: Teléfono (opcional)
    - **bio**: Biografía (opcional)
    - **avatar_url**: URL del avatar (opcional)
    
    Requiere autenticación
    """
    user_service = UserService(db)
    return await user_service.update_user(user_id, user_data)

@router.post("/me/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: TokenData = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cambiar contraseña del usuario actual
    
    - **current_password**: Contraseña actual
    - **new_password**: Nueva contraseña
    - **confirm_password**: Confirmación de nueva contraseña
    
    Requiere autenticación
    """
    user_service = UserService(db)
    await user_service.change_password(current_user.user_id, password_data)
    return {"message": "Contraseña cambiada exitosamente"}

@router.delete("/{user_id}")
async def delete_user(
    user_id: int = Path(..., description="ID del usuario"),
    current_user: TokenData = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Desactivar usuario por ID
    
    - **user_id**: ID del usuario a desactivar
    
    Requiere autenticación
    """
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    return {"message": "Usuario desactivado exitosamente"}

@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: int = Path(..., description="ID del usuario"),
    current_user: TokenData = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Activar usuario por ID
    
    - **user_id**: ID del usuario a activar
    
    Requiere autenticación
    """
    user_service = UserService(db)
    return await user_service.activate_user(user_id)
