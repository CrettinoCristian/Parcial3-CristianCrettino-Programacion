#!/usr/bin/env python3
"""
Script para inicializar la base de datos en producción (SQLite)
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db

def init_production_db():
    """Inicializa la base de datos SQLite para producción"""
    app = create_app('production')
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Base de datos SQLite inicializada correctamente para producción")

if __name__ == '__main__':
    init_production_db()