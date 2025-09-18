import os
from datetime import timedelta

class Config:
    """Configuración base para la aplicación Flask"""
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f5a3b2c8e4d90123a9b7c4d5f6e7a8b9'
    
    # Configuración de la base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configuración de Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # Configuración de archivos estáticos
    UPLOAD_FOLDER = 'static/images'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    # PostgreSQL para desarrollo local
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:612345621c@localhost:5432/mini_crm'
    
class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    
    # Buscar variables de PostgreSQL en orden de prioridad
    # Vercel Postgres requiere parámetros SSL específicos
    database_url = (
        os.environ.get('POSTGRES_URL') or 
        os.environ.get('DATABASE_URL') or 
        os.environ.get('POSTGRES_DATABASE') or
        os.environ.get('POSTGRES_PRISMA_URL') or
        'postgresql://postgres:612345621c@localhost:5432/mini_crm'
    )
    
    # Agregar parámetros SSL para Vercel Postgres si es necesario
    if database_url and 'vercel-storage.com' in database_url:
        if '?' not in database_url:
            database_url += '?sslmode=require'
        elif 'sslmode' not in database_url:
            database_url += '&sslmode=require'
    
    SQLALCHEMY_DATABASE_URI = database_url

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}