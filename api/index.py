import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Crear la aplicación Flask para producción
app = create_app('production')

# Esta es la función que Vercel utilizará como punto de entrada
if __name__ == "__main__":
    app.run()