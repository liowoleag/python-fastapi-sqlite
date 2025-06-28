"""
Repositorio para operaciones de usuario en base de datos
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.exc import IntegrityError
import logging

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.core.exceptions import ConflictException, NotFoundException

logger = logging.getLogger(__name__)

class UserRepository:
    """Repositorio para operaciones CRUD de usuarios"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_data: UserCreate) -> User:
        """Crear un nuevo usuario"""
        try:
            # Crear instancia del usuario
            db_user = User(
                email=user_data.email,
                username=user_data.username,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                hashed_password=get_password_hash(user_data.password),
                phone=user_data.phone,
                bio=user_data.bio,
                avatar_url=user_data.avatar_url
            )
            
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            
            logger.info(f"Usuario creado: {db_user.username}")
            return db_user
            
        except IntegrityError as e:
            await self.db.rollback()
            logger.warning(f"Error de integridad al crear usuario: {e}")
            
            if "email" in str(e):
                raise ConflictException("El email ya está registrado")
            elif "username" in str(e):
                raise ConflictException("El nombre de usuario ya está en uso")
            else:
                raise ConflictException("Error de datos duplicados")
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 20,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> tuple[List[User], int]:
        """Obtener lista de usuarios con paginación y filtros"""
        
        # Construir query base
        query = select(User)
        count_query = select(func.count(User.id))
        
        # Aplicar filtros
        if search:
            search_filter = or_(
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
            count_query = count_query.where(User.is_active == is_active)
        
        # Aplicar paginación
        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        
        # Ejecutar queries
        result = await self.db.execute(query)
        count_result = await self.db.execute(count_query)
        
        users = result.scalars().all()
        total = count_result.scalar()
        
        return users, total
    
    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        """Actualizar usuario"""
        db_user = await self.get_by_id(user_id)
        if not db_user:
            raise NotFoundException("Usuario no encontrado")
        
        # Actualizar solo los campos proporcionados
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        try:
            await self.db.commit()
            await self.db.refresh(db_user)
            logger.info(f"Usuario actualizado: {db_user.username}")
            return db_user
        except IntegrityError as e:
            await self.db.rollback()
            logger.warning(f"Error de integridad al actualizar usuario: {e}")
            raise ConflictException("Error al actualizar: datos duplicados")
    
    async def delete(self, user_id: int) -> bool:
        """Eliminar usuario (soft delete)"""
        db_user = await self.get_by_id(user_id)
        if not db_user:
            raise NotFoundException("Usuario no encontrado")
        
        db_user.is_active = False
        await self.db.commit()
        
        logger.info(f"Usuario desactivado: {db_user.username}")
        return True
    
    async def hard_delete(self, user_id: int) -> bool:
        """Eliminar usuario permanentemente"""
        db_user = await self.get_by_id(user_id)
        if not db_user:
            raise NotFoundException("Usuario no encontrado")
        
        await self.db.delete(db_user)
        await self.db.commit()
        
        logger.info(f"Usuario eliminado permanentemente: {db_user.username}")
        return True
    
    async def change_password(self, user_id: int, new_password: str) -> User:
        """Cambiar contraseña de usuario"""
        db_user = await self.get_by_id(user_id)
        if not db_user:
            raise NotFoundException("Usuario no encontrado")
        
        db_user.hashed_password = get_password_hash(new_password)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        logger.info(f"Contraseña cambiada para usuario: {db_user.username}")
        return db_user
