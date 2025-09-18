#!/usr/bin/env python3
"""
Script para inicializar la base de datos en Vercel
Este script se puede ejecutar manualmente para crear las tablas
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User
import bcrypt

def init_vercel_database():
    """Inicializar la base de datos en Vercel con datos de prueba"""
    
    # Crear la aplicación en modo producción
    app = create_app('production')
    
    with app.app_context():
        try:
            print("🔄 Eliminando tablas existentes...")
            db.drop_all()
            
            print("🔄 Creando nuevas tablas...")
            db.create_all()
            
            print("🔄 Verificando que las tablas se crearon...")
            # Verificar que las tablas existen
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tablas creadas: {tables}")
            
            # Crear usuario de prueba si no existe
            test_email = "crettinocristian@gmail.com"
            existing_user = User.query.filter_by(email=test_email).first()
            
            if not existing_user:
                print(f"👤 Creando usuario de prueba: {test_email}")
                test_user = User(
                    nombre="Cristian Crettino",
                    email=test_email
                )
                test_user.set_password("123456")
                
                db.session.add(test_user)
                db.session.commit()
                print("✅ Usuario de prueba creado exitosamente")
            else:
                print("👤 Usuario de prueba ya existe")
            
            print("✅ Base de datos inicializada correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = init_vercel_database()
    sys.exit(0 if success else 1)