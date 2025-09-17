from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modelo de usuario para autenticación"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con contactos
    contactos = db.relationship('Contacto', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hashea y guarda la contraseña"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.email}>'

class Contacto(db.Model):
    """Modelo de contacto del CRM"""
    __tablename__ = 'contactos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    empresa = db.Column(db.String(100), nullable=True)
    etiquetas = db.Column(ARRAY(db.String), nullable=True, default=[])
    notas = db.Column(db.Text, nullable=True)
    ultima_interaccion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con interacciones
    interacciones = db.relationship('Interaccion', backref='contacto', lazy=True, cascade='all, delete-orphan')
    
    def actualizar_ultima_interaccion(self):
        """Actualiza la fecha de última interacción"""
        self.ultima_interaccion = datetime.utcnow()
        self.fecha_actualizacion = datetime.utcnow()
    
    def get_etiquetas_str(self):
        """Retorna las etiquetas como string separado por comas"""
        return ', '.join(self.etiquetas) if self.etiquetas else ''
    
    def set_etiquetas_from_str(self, etiquetas_str):
        """Establece las etiquetas desde un string separado por comas"""
        if etiquetas_str:
            self.etiquetas = [tag.strip() for tag in etiquetas_str.split(',') if tag.strip()]
        else:
            self.etiquetas = []
    
    def __repr__(self):
        return f'<Contacto {self.nombre}>'

class Interaccion(db.Model):
    """Modelo de interacción con contactos"""
    __tablename__ = 'interacciones'
    
    id = db.Column(db.Integer, primary_key=True)
    contacto_id = db.Column(db.Integer, db.ForeignKey('contactos.id'), nullable=False, index=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    nota = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Interaccion {self.id} - {self.fecha}>'