#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos de Vercel
"""
import os
import sys
import psycopg2
from urllib.parse import urlparse

def test_vercel_connection():
    """Probar conexión directa a la base de datos de Vercel"""
    
    # URL de PostgreSQL de Vercel (desde los logs)
    postgres_url = "postgresql://neondb_owner:npg_Zt7ykeCTOwr0@ep-flat-resonance-ad2muymd-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
    
    try:
        print("🔄 Probando conexión a PostgreSQL de Vercel...")
        print(f"URL: {postgres_url}")
        
        # Parsear la URL
        parsed = urlparse(postgres_url)
        print(f"Host: {parsed.hostname}")
        print(f"Database: {parsed.path[1:]}")
        print(f"User: {parsed.username}")
        print(f"SSL Mode: require")
        
        # Intentar conexión
        conn = psycopg2.connect(postgres_url)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa!")
        
        # Verificar tablas existentes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"📋 Tablas encontradas: {[table[0] for table in tables]}")
        
        # Verificar si existe la tabla users
        if any('users' in table for table in tables):
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"👥 Usuarios en la base de datos: {user_count}")
            
            # Mostrar usuarios existentes
            cursor.execute("SELECT id, nombre, email FROM users LIMIT 5")
            users = cursor.fetchall()
            print("👤 Usuarios existentes:")
            for user in users:
                print(f"  - ID: {user[0]}, Nombre: {user[1]}, Email: {user[2]}")
        else:
            print("❌ Tabla 'users' no encontrada")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    success = test_vercel_connection()
    sys.exit(0 if success else 1)