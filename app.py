from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import datetime
from config import config
from models import db, User

def create_app(config_name='development'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Para producción en Vercel, configurar instance_path en directorio temporal
    if config_name == 'production':
        app.instance_path = '/tmp'
    
    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Filtros personalizados de Jinja2
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convierte saltos de línea en etiquetas <br>"""
        if text is None:
            return ''
        return text.replace('\n', '<br>\n')
    
    # Funciones globales de Jinja2
    @app.template_global()
    def now():
        """Devuelve la fecha y hora actual"""
        return datetime.now()
    
    # Registrar blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.contactos import contactos_bp
    from routes.interacciones import interacciones_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(contactos_bp)
    app.register_blueprint(interacciones_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)