import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db

# Crear la aplicación Flask para producción
app = create_app('production')

# Debug: Imprimir variables de entorno importantes
print(f"[DEBUG] FLASK_ENV: {os.environ.get('FLASK_ENV', 'Not set')}")
print(f"[DEBUG] SECRET_KEY: {'Set' if os.environ.get('SECRET_KEY') else 'Not set'}")
print(f"[DEBUG] POSTGRES_URL: {'Set' if os.environ.get('POSTGRES_URL') else 'Not set'}")
print(f"[DEBUG] DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")
print(f"[DEBUG] POSTGRES_DATABASE: {'Set' if os.environ.get('POSTGRES_DATABASE') else 'Not set'}")
print(f"[DEBUG] POSTGRES_PRISMA_URL: {'Set' if os.environ.get('POSTGRES_PRISMA_URL') else 'Not set'}")
print(f"[DEBUG] POSTGRES_URL_NON_POOLING: {'Set' if os.environ.get('POSTGRES_URL_NON_POOLING') else 'Not set'}")

# Mostrar la URL de base de datos que se está usando (sin credenciales)
db_url = (
    os.environ.get('POSTGRES_URL') or 
    os.environ.get('DATABASE_URL') or 
    os.environ.get('POSTGRES_DATABASE') or
    os.environ.get('POSTGRES_PRISMA_URL') or
    'fallback'
)

if db_url != 'fallback':
    # Ocultar credenciales para logging seguro
    safe_url = db_url.split('@')[1] if '@' in db_url else db_url
    print(f"[DEBUG] Using database: {safe_url}")
    
    # Verificar si es Vercel Postgres
    if 'vercel-storage.com' in db_url:
        print("[DEBUG] Detected Vercel Postgres - SSL required")
        if 'sslmode' not in db_url:
            print("[DEBUG] Adding SSL mode to database URL")
    else:
        print("[DEBUG] Not Vercel Postgres - standard connection")
else:
    print("[DEBUG] Using fallback database URL")

# Inicializar la base de datos si no existe
with app.app_context():
    try:
        # Verificar si las tablas existen
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        print(f"[DEBUG] Existing tables: {existing_tables}")
        
        if not existing_tables or 'users' not in existing_tables:
            print("[DEBUG] Creating database tables...")
            db.create_all()
            print("[DEBUG] Database tables created successfully")
            
            # Crear usuario de prueba si no existe
            from models import User
            test_user = User.query.filter_by(email="crettinocristian@gmail.com").first()
            if not test_user:
                print("[DEBUG] Creating test user...")
                test_user = User(nombre="Cristian Crettino", email="crettinocristian@gmail.com")
                test_user.set_password("123456")
                db.session.add(test_user)
                db.session.commit()
                print("[DEBUG] Test user created successfully")
        else:
            print("[DEBUG] Database tables already exist")
            
    except Exception as e:
        print(f"[DEBUG] Error inicializando base de datos: {e}")
        # Intentar crear las tablas de todas formas
        try:
            db.create_all()
            print("[DEBUG] Tables created after error")
        except Exception as e2:
            print(f"[DEBUG] Failed to create tables: {e2}")

# Vercel necesita que la aplicación se exporte directamente
# No usar if __name__ == "__main__" en funciones serverless