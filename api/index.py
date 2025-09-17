import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db

# Crear la aplicación Flask para producción
app = create_app('production')

# Inicializar la base de datos SQLite si no existe
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")

# Vercel necesita que la aplicación se exporte directamente
# No usar if __name__ == "__main__" en funciones serverless