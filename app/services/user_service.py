"""
Servicio de lógica de negocio para usuarios
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserList, PasswordChange
from app.core.security import verify_password
from app.core.exceptions import ValidationException, UnauthorizedException
from app.core.config import settings

logger = logging.getLogger(__name__)

class UserService:
    """Servicio para lógica de negocio de usuarios"""
    
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Crear un nuevo usuario con validaciones de negocio"""
        
        # Validaciones adicionales de negocio
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValidationException("El email ya está registrado")
        
        existing_username = await self.repository.get_by_username(user_data.username)
        if existing_username:
            raise ValidationException("El nombre de usuario ya está en uso")
        
        # Crear usuario
        db_user = await self.repository.create(user_data)
        
        logger.info(f"Nuevo usuario registrado: {db_user.email}")
        return UserResponse.from_orm(db_user)
    
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        """Obtener usuario por ID"""
        db_user = await self.repository.get_by_id(user_id)
        if not db_user:
            raise ValidationException("Usuario no encontrado")
        
        return UserResponse.from_orm(db_user)
    
    async def get_users(
        self,
        page: int = 1,
        size: int = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> UserList:
        """Obtener lista paginada de usuarios"""
        
        # Validar parámetros de paginación
        if page < 1:
            raise ValidationException("El número de página debe ser mayor a 0")
        
        if size is None:
            size = settings.DEFAULT_PAGE_SIZE
        elif size > settings.MAX_PAGE_SIZE:
            size = settings.MAX_PAGE_SIZE
        elif size < 1:
            raise ValidationException("El tamaño de página debe ser mayor a 0")
        
        skip = (page - 1) * size
        
        users, total = await self.repository.get_all(
            skip=skip,
            limit=size,
            search=search,
            is_active=is_active
        )
        
        # Calcular número total de páginas
        pages = (total + size - 1) // size
        
        return UserList(
            users=[UserResponse.from_orm(user) for user in users],
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Actualizar usuario"""
        db_user = await self.repository.update(user_id, user_data)
        
        logger.info(f"Usuario actualizado: {db_user.email}")
        return UserResponse.from_orm(db_user)
    
    async def delete_user(self, user_id: int) -> bool:
        """Desactivar usuario"""
        result = await self.repository.delete(user_id)
        
        logger.info(f"Usuario desactivado: ID {user_id}")
        return result
    
    async def change_password(self, user_id: int, password_data: PasswordChange) -> bool:
        """Cambiar contraseña de usuario"""
        
        # Obtener usuario actual
        db_user = await self.repository.get_by_id(user_id)
        if not db_user:
            raise ValidationException("Usuario no encontrado")
        
        # Verificar contraseña actual
        if not verify_password(password_data.current_password, db_user.hashed_password):
            raise UnauthorizedException("Contraseña actual incorrecta")
        
        # Cambiar contraseña
        await self.repository.change_password(user_id, password_data.new_password)
        
        logger.info(f"Contraseña cambiada para usuario: {db_user.email}")
        return True
    
    async def activate_user(self, user_id: int) -> UserResponse:
        """Activar usuario"""
        db_user = await self.repository.get_by_id(user_id)
        if not db_user:
            raise ValidationException("Usuario no encontrado")
        
        update_data = UserUpdate()
        db_user = await self.repository.update(user_id, update_data)
        
        # Activar manualmente
        db_user.is_active = True
        await self.repository.db.commit()
        await self.repository.db.refresh(db_user)
        
        logger.info(f"Usuario activado: {db_user.email}")
        return UserResponse.from_orm(db_user)
