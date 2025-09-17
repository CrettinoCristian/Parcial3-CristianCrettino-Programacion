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
    # SQLite para producción en Vercel (más simple y sin configuración adicional)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///mini_crm.db'

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}