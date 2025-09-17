#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialización de la base de datos para Mini CRM Personal

Este script:
1. Crea las tablas de la base de datos
2. Inicializa las migraciones de Flask-Migrate
3. Opcionalmente carga datos de ejemplo

Uso:
    python init_db.py [--sample-data]
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
from app import create_app
from models import db, User, Contacto, Interaccion
from flask_migrate import init, migrate, upgrade
from sqlalchemy import text

def init_database(app):
    """Inicializa la base de datos y las migraciones"""
    with app.app_context():
        try:
            # Crear todas las tablas
            print("Creando tablas de la base de datos...")
            db.create_all()
            print("✓ Tablas creadas exitosamente")
            
            # Inicializar migraciones si no existen
            migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
            if not os.path.exists(migrations_dir):
                print("Inicializando migraciones...")
                init()
                print("✓ Migraciones inicializadas")
            else:
                print("✓ Migraciones ya existen")
            
            return True
            
        except Exception as e:
            print(f"✗ Error inicializando la base de datos: {str(e)}")
            return False

def create_sample_data(app):
    """Crea datos de ejemplo para pruebas"""
    with app.app_context():
        try:
            print("Creando datos de ejemplo...")
            
            # Verificar si ya existen usuarios
            if User.query.first():
                print("✓ Ya existen datos en la base de datos")
                return True
            
            # Crear usuario de ejemplo
            usuario_demo = User(
                nombre="Usuario Demo",
                email="demo@minicrm.com"
            )
            usuario_demo.set_password("demo123")
            db.session.add(usuario_demo)
            db.session.flush()  # Para obtener el ID
            
            # Crear contactos de ejemplo
            contactos_ejemplo = [
                {
                    "nombre": "Juan Pérez",
                    "email": "juan.perez@empresa.com",
                    "telefono": "+1234567890",
                    "empresa": "Empresa ABC",
                    "etiquetas": ["cliente", "importante"],
                    "notas": "Cliente principal de la empresa. Muy interesado en nuestros servicios."
                },
                {
                    "nombre": "María García",
                    "email": "maria.garcia@startup.com",
                    "telefono": "+0987654321",
                    "empresa": "Startup XYZ",
                    "etiquetas": ["prospecto", "tecnología"],
                    "notas": "Fundadora de startup tecnológica. Potencial colaboración."
                },
                {
                    "nombre": "Carlos López",
                    "email": "carlos.lopez@proveedor.com",
                    "telefono": "+1122334455",
                    "empresa": "Proveedores SA",
                    "etiquetas": ["proveedor", "confiable"],
                    "notas": "Proveedor de servicios de calidad. Excelente relación comercial."
                },
                {
                    "nombre": "Ana Martínez",
                    "email": "ana.martinez@consultora.com",
                    "telefono": "+5566778899",
                    "empresa": "Consultora Estratégica",
                    "etiquetas": ["consultor", "estrategia"],
                    "notas": "Consultora especializada en estrategia empresarial."
                },
                {
                    "nombre": "Roberto Silva",
                    "email": "roberto.silva@freelance.com",
                    "telefono": "+9988776655",
                    "empresa": "Freelancer",
                    "etiquetas": ["freelancer", "diseño"],
                    "notas": "Diseñador gráfico freelancer. Trabajos de alta calidad."
                }
            ]
            
            contactos_creados = []
            for contacto_data in contactos_ejemplo:
                contacto = Contacto(
                    user_id=usuario_demo.id,
                    nombre=contacto_data["nombre"],
                    email=contacto_data["email"],
                    telefono=contacto_data["telefono"],
                    empresa=contacto_data["empresa"],
                    notas=contacto_data["notas"],
                    fecha_creacion=datetime.now() - timedelta(days=len(contactos_creados) * 2)  # Usar hora local
                )
                contacto.etiquetas = contacto_data["etiquetas"]
                db.session.add(contacto)
                contactos_creados.append(contacto)
            
            db.session.flush()  # Para obtener los IDs de los contactos
            
            # Crear interacciones de ejemplo
            interacciones_ejemplo = [
                {
                    "contacto": contactos_creados[0],
                    "nota": "Llamada inicial para presentar nuestros servicios. Mostró mucho interés en la propuesta.",
                    "dias_atras": 5
                },
                {
                    "contacto": contactos_creados[0],
                    "nota": "Reunión presencial en sus oficinas. Discutimos detalles del proyecto y presupuesto.",
                    "dias_atras": 3
                },
                {
                    "contacto": contactos_creados[1],
                    "nota": "Intercambio de emails sobre posible colaboración. Enviamos propuesta inicial.",
                    "dias_atras": 7
                },
                {
                    "contacto": contactos_creados[1],
                    "nota": "Seguimiento telefónico. Están evaluando la propuesta internamente.",
                    "dias_atras": 2
                },
                {
                    "contacto": contactos_creados[2],
                    "nota": "Reunión para revisar términos del contrato de proveeduría. Todo en orden.",
                    "dias_atras": 10
                },
                {
                    "contacto": contactos_creados[3],
                    "nota": "Consulta sobre servicios de consultoría estratégica. Programamos reunión.",
                    "dias_atras": 4
                },
                {
                    "contacto": contactos_creados[4],
                    "nota": "Revisión de diseños para el nuevo proyecto. Excelente trabajo como siempre.",
                    "dias_atras": 1
                }
            ]
            
            for interaccion_data in interacciones_ejemplo:
                interaccion = Interaccion(
                    contacto_id=interaccion_data["contacto"].id,
                    nota=interaccion_data["nota"],
                    fecha=datetime.now() - timedelta(days=interaccion_data["dias_atras"])  # Usar hora local
                )
                db.session.add(interaccion)
                
                # Actualizar última interacción del contacto
                interaccion_data["contacto"].actualizar_ultima_interaccion()
            
            # Guardar todos los cambios
            db.session.commit()
            
            print(f"✓ Datos de ejemplo creados:")
            print(f"  - 1 usuario demo (email: demo@minicrm.com, password: demo123)")
            print(f"  - {len(contactos_ejemplo)} contactos")
            print(f"  - {len(interacciones_ejemplo)} interacciones")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error creando datos de ejemplo: {str(e)}")
            return False

def check_database_connection(app):
    """Verifica la conexión a la base de datos"""
    with app.app_context():
        try:
            # Intentar una consulta simple
            db.session.execute(text('SELECT 1'))
            print("✓ Conexión a la base de datos exitosa")
            return True
        except Exception as e:
            print(f"✗ Error conectando a la base de datos: {str(e)}")
            print("\nVerifica que:")
            print("1. PostgreSQL esté ejecutándose")
            print("2. La base de datos 'mini_crm' exista")
            print("3. Las credenciales en config.py sean correctas")
            return False

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Inicializar base de datos Mini CRM')
    parser.add_argument('--sample-data', action='store_true', 
                       help='Crear datos de ejemplo para pruebas')
    parser.add_argument('--check-only', action='store_true',
                       help='Solo verificar la conexión a la base de datos')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Mini CRM Personal - Inicialización de Base de Datos")
    print("=" * 50)
    
    # Crear la aplicación
    app = create_app('development')
    
    # Verificar conexión
    if not check_database_connection(app):
        sys.exit(1)
    
    if args.check_only:
        print("\n✓ Verificación completada")
        return
    
    # Inicializar base de datos
    if not init_database(app):
        sys.exit(1)
    
    # Crear datos de ejemplo si se solicita
    if args.sample_data:
        if not create_sample_data(app):
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✓ Inicialización completada exitosamente")
    print("=" * 50)
    
    if args.sample_data:
        print("\nPuedes iniciar sesión con:")
        print("Email: demo@minicrm.com")
        print("Password: demo123")
    
    print("\nPara iniciar la aplicación ejecuta:")
    print("python app.py")
    print("\nLuego visita: http://localhost:5000")

if __name__ == '__main__':
    main()