from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from models import db, Contacto, Interaccion
from sqlalchemy import func, desc
from collections import Counter
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página de inicio"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del usuario"""
    # Obtener estadísticas del usuario
    total_contactos = Contacto.query.filter_by(user_id=current_user.id).count()
    
    # Últimos 5 contactos agregados
    ultimos_contactos = Contacto.query.filter_by(user_id=current_user.id)\
                                     .order_by(desc(Contacto.fecha_creacion))\
                                     .limit(5).all()
    
    # Total de interacciones
    total_interacciones = db.session.query(func.count(Interaccion.id))\
                                   .join(Contacto)\
                                   .filter(Contacto.user_id == current_user.id)\
                                   .scalar()
    
    # Generar gráfico de etiquetas
    grafico_etiquetas = generar_grafico_etiquetas(current_user.id)
    
    return render_template('dashboard.html', 
                         total_contactos=total_contactos,
                         ultimos_contactos=ultimos_contactos,
                         total_interacciones=total_interacciones,
                         grafico_etiquetas=grafico_etiquetas)

def generar_grafico_etiquetas(user_id):
    """Genera datos de distribución de etiquetas (versión simplificada)"""
    try:
        # Obtener todos los contactos del usuario
        contactos = Contacto.query.filter_by(user_id=user_id).all()
        
        # Contar etiquetas
        todas_etiquetas = []
        for contacto in contactos:
            if contacto.etiquetas_list:
                todas_etiquetas.extend(contacto.etiquetas_list)
        
        if not todas_etiquetas:
            return None
        
        # Contar frecuencia de etiquetas
        contador_etiquetas = Counter(todas_etiquetas)
        
        # Retornar datos para mostrar en tabla
        return dict(contador_etiquetas.most_common(10))
        
    except Exception as e:
        current_app.logger.error(f'Error generando datos de etiquetas: {str(e)}')
        return None

@main_bp.route('/about')
def about():
    """Página acerca de"""
    return render_template('about.html')