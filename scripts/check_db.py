"""
Script para verificar el estado de la base de datos SQLite
"""
import asyncio
import sys
import os
import sqlite3

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal, engine
from sqlalchemy import text

async def check_database():
    """Verificar estado de la base de datos"""
    
    print("🔍 Verificando base de datos SQLite...")
    
    # Verificar archivo de base de datos
    db_file = "./users.db"
    if os.path.exists(db_file):
        file_size = os.path.getsize(db_file)
        print(f"✅ Archivo de base de datos existe: {db_file}")
        print(f"   Tamaño: {file_size} bytes")
    else:
        print(f"❌ Archivo de base de datos no existe: {db_file}")
        return
    
    # Verificar conexión async
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = result.fetchall()
            
            print(f"✅ Conexión async exitosa")
            print(f"📊 Tablas encontradas: {len(tables)}")
            
            for table in tables:
                print(f"   - {table[0]}")
                
                # Contar registros en cada tabla
                if table[0] != 'sqlite_sequence':
                    count_result = await db.execute(text(f"SELECT COUNT(*) FROM {table[0]};"))
                    count = count_result.scalar()
                    print(f"     Registros: {count}")
    
    except Exception as e:
        print(f"❌ Error en conexión async: {e}")
    
    # Verificar con sqlite3 directo
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"✅ Conexión directa SQLite exitosa")
        
        if 'users' in [table[0] for table in tables]:
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"👥 Usuarios en la base de datos: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT id, email, username, is_active, is_superuser FROM users LIMIT 5;")
                users = cursor.fetchall()
                print("📋 Primeros usuarios:")
                for user in users:
                    print(f"   ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Active: {user[3]}, Super: {user[4]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en conexión directa: {e}")

if __name__ == "__main__":
    asyncio.run(check_database())
