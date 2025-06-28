"""
Script para crear usuario administrador
"""
import asyncio
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal
from app.services.user_service import UserService
from app.schemas.user import UserCreate

async def create_admin_user():
    """Crear usuario administrador"""
    
    admin_data = UserCreate(
        email="admin@example.com",
        username="admin",
        first_name="Admin",
        last_name="User",
        password="Admin123!",
        confirm_password="Admin123!",
        bio="Usuario administrador del sistema"
    )
    
    async with AsyncSessionLocal() as db:
        user_service = UserService(db)
        
        try:
            # Verificar si ya existe un admin
            from app.repositories.user_repository import UserRepository
            repo = UserRepository(db)
            existing_admin = await repo.get_by_email("admin@example.com")
            
            if existing_admin:
                print("❌ El usuario administrador ya existe:")
                print(f"   Email: {existing_admin.email}")
                print(f"   Username: {existing_admin.username}")
                return
            
            admin_user = await user_service.create_user(admin_data)
            print(f"✅ Usuario administrador creado exitosamente:")
            print(f"   ID: {admin_user.id}")
            print(f"   Email: {admin_user.email}")
            print(f"   Username: {admin_user.username}")
            
            # Hacer superusuario
            repo = UserRepository(db)
            db_user = await repo.get_by_id(admin_user.id)
            db_user.is_superuser = True
            await db.commit()
            
            print("✅ Usuario marcado como superusuario")
            print("\n🔑 Credenciales de acceso:")
            print("   Email: admin@example.com")
            print("   Password: Admin123!")
            
        except Exception as e:
            print(f"❌ Error al crear usuario administrador: {e}")

if __name__ == "__main__":
    print("🚀 Creando usuario administrador...")
    asyncio.run(create_admin_user())
