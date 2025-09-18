import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de base de datos
    # Prioridad: POSTGRES_URL (Vercel) > DATABASE_URL (Neon/Railway/Supabase) > SQLite local
    POSTGRES_URL = os.environ.get('POSTGRES_URL')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if POSTGRES_URL:
        # Vercel PostgreSQL
        SQLALCHEMY_DATABASE_URI = POSTGRES_URL
        print(f"[CONFIG] Using Vercel PostgreSQL: {POSTGRES_URL[:50]}...")
    elif DATABASE_URL:
        # Neon, Railway, Supabase, u otra PostgreSQL
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        # Detectar proveedor por la URL
        if 'neon.tech' in DATABASE_URL:
            print(f"[CONFIG] Using Neon PostgreSQL: {DATABASE_URL[:50]}...")
        elif 'railway.app' in DATABASE_URL:
            print(f"[CONFIG] Using Railway PostgreSQL: {DATABASE_URL[:50]}...")
        elif 'supabase.co' in DATABASE_URL:
            print(f"[CONFIG] Using Supabase PostgreSQL: {DATABASE_URL[:50]}...")
        else:
            print(f"[CONFIG] Using PostgreSQL: {DATABASE_URL[:50]}...")
    else:
        # SQLite local para desarrollo
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "app.db")}'
        print("[CONFIG] Using local SQLite database")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración específica para PostgreSQL
    if 'postgresql://' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'connect_args': {
                'sslmode': 'require' if 'sslmode=require' not in SQLALCHEMY_DATABASE_URI else None
            }
        }
    
    # Configuración de Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

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