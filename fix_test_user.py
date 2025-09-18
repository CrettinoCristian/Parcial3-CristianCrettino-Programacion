#!/usr/bin/env python3
"""
Script para arreglar la contraseña del usuario de prueba
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User

def fix_test_user():
    """Arreglar la contraseña del usuario de prueba"""
    
    # Crear la aplicación en modo producción
    app = create_app('production')
    
    with app.app_context():
        try:
            print("🔄 Arreglando usuario de prueba...")
            
            # Buscar el usuario de prueba
            test_email = "crettinocristian@gmail.com"
            user = User.query.filter_by(email=test_email).first()
            
            if not user:
                print(f"❌ Usuario {test_email} no encontrado")
                return False
            
            print(f"✅ Usuario encontrado: {user.nombre}")
            print(f"🔐 Hash anterior: {user.password_hash[:30]}...")
            
            # Actualizar la contraseña
            new_password = "123456"
            user.set_password(new_password)
            
            # Guardar cambios
            db.session.commit()
            
            print(f"🔐 Nuevo hash: {user.password_hash[:30]}...")
            
            # Verificar que funciona
            if user.check_password(new_password):
                print("✅ Contraseña actualizada correctamente")
                print(f"📧 Email: {test_email}")
                print(f"🔑 Contraseña: {new_password}")
                return True
            else:
                print("❌ Error: La contraseña sigue sin funcionar")
                return False
            
        except Exception as e:
            print(f"❌ Error arreglando usuario: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = fix_test_user()
    sys.exit(0 if success else 1)