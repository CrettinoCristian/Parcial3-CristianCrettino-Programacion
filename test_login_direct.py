#!/usr/bin/env python3
"""
Script para probar el proceso de login directamente
"""
import os
import sys
import bcrypt

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User

def test_login_process():
    """Probar el proceso completo de login"""
    
    # Crear la aplicación en modo producción
    app = create_app('production')
    
    with app.app_context():
        try:
            print("🔄 Probando proceso de login...")
            
            # Buscar el usuario de prueba
            test_email = "crettinocristian@gmail.com"
            user = User.query.filter_by(email=test_email).first()
            
            if not user:
                print(f"❌ Usuario {test_email} no encontrado")
                return False
            
            print(f"✅ Usuario encontrado: {user.nombre} ({user.email})")
            print(f"📅 Fecha de creación: {user.fecha_creacion}")
            print(f"🔐 Hash de contraseña: {user.password_hash[:20]}...")
            
            # Probar la contraseña
            test_password = "123456"
            print(f"🔄 Probando contraseña: {test_password}")
            
            # Verificar contraseña usando el método del modelo
            password_valid = user.check_password(test_password)
            print(f"✅ Contraseña válida: {password_valid}")
            
            if not password_valid:
                print("❌ La contraseña no coincide")
                
                # Intentar verificar manualmente
                try:
                    manual_check = bcrypt.checkpw(
                        test_password.encode('utf-8'), 
                        user.password_hash.encode('utf-8')
                    )
                    print(f"🔄 Verificación manual: {manual_check}")
                except Exception as e:
                    print(f"❌ Error en verificación manual: {e}")
                
                return False
            
            print("✅ Proceso de login exitoso")
            return True
            
        except Exception as e:
            print(f"❌ Error en proceso de login: {e}")
            return False

if __name__ == "__main__":
    success = test_login_process()
    sys.exit(0 if success else 1)