"""
Script para forzar la creación de la base de datos y tablas
"""
import asyncio
import sys
import os
import sqlite3

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models.user import User  # Importar el modelo
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def force_create_database():
    """Forzar creación de base de datos y tablas"""
    
    print("🔧 Forzando creación de base de datos SQLite...")
    
    try:
        # Eliminar base de datos existente si hay problemas
        db_file = "./users.db"
        if os.path.exists(db_file):
            print(f"🗑️  Eliminando base de datos existente: {db_file}")
            os.remove(db_file)
        
        # Verificar que el modelo está registrado
        print(f"📋 Modelos registrados: {list(Base.metadata.tables.keys())}")
        
        # Crear todas las tablas
        async with engine.begin() as conn:
            print("🏗️  Creando tablas...")
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tablas creadas con SQLAlchemy")
        
        # Verificar con SQLite directo
        if os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Ver tablas creadas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"📊 Tablas en SQLite: {[table[0] for table in tables]}")
            
            # Ver estructura de la tabla users
            if any(table[0] == 'users' for table in tables):
                cursor.execute("PRAGMA table_info(users)")
                columns = cursor.fetchall()
                print(f"🏗️  Columnas de tabla users:")
                for col in columns:
                    print(f"   - {col[1]} ({col[2]})")
                
                # Insertar usuario de prueba
                cursor.execute("""
                    INSERT INTO users (
                        email, username, first_name, last_name, 
                        hashed_password, is_active, is_superuser,
                        created_at
                    ) VALUES (
                        'test@example.com', 'testuser', 'Test', 'User',
                        '$2b$12$test.hash.for.testing', 1, 0,
                        datetime('now')
                    )
                """)
                conn.commit()
                print("✅ Usuario de prueba insertado")
                
                # Verificar inserción
                cursor.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
                print(f"👥 Total usuarios: {count}")
            
            conn.close()
        
        print("🎉 Base de datos creada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(force_create_database())
