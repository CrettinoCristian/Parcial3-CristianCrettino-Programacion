from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models import Contacto, Interaccion, db
from sqlalchemy import func, desc
from collections import Counter
from utils.statistics import (
    generar_grafico_etiquetas, 
    generar_grafico_interacciones_tiempo,
    generar_grafico_contactos_empresa,
    obtener_estadisticas_generales
)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página de inicio"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del usuario con estadísticas completas"""
    try:
        # Obtener estadísticas generales
        estadisticas = obtener_estadisticas_generales(current_user.id)
        
        # Últimos 5 contactos agregados
        ultimos_contactos = Contacto.query.filter_by(user_id=current_user.id)\
                                         .order_by(desc(Contacto.fecha_creacion))\
                                         .limit(5).all()
        
        # Generar gráficos usando las funciones del módulo statistics
        resultado_etiquetas = generar_grafico_etiquetas(current_user.id)
        if resultado_etiquetas and len(resultado_etiquetas) == 2:
            grafico_etiquetas_img, grafico_etiquetas_data = resultado_etiquetas
        else:
            grafico_etiquetas_img, grafico_etiquetas_data = None, None
            
        grafico_interacciones_img = generar_grafico_interacciones_tiempo(current_user.id)
        grafico_empresas_img = generar_grafico_contactos_empresa(current_user.id)
        
        # Si no hay datos de etiquetas del módulo, usar función de fallback
        if not grafico_etiquetas_data:
            grafico_etiquetas_data = generar_grafico_etiquetas_fallback(current_user.id)
        
        return render_template('dashboard.html', 
                             estadisticas=estadisticas,
                             ultimos_contactos=ultimos_contactos,
                             grafico_etiquetas_img=grafico_etiquetas_img,
                             grafico_etiquetas_data=grafico_etiquetas_data,
                             grafico_interacciones_img=grafico_interacciones_img,
                             grafico_empresas_img=grafico_empresas_img,
                             # Mantener compatibilidad con template actual
                             total_contactos=estadisticas['total_contactos'],
                             total_interacciones=estadisticas['total_interacciones'],
                             grafico_etiquetas=grafico_etiquetas_data)
                             
    except Exception as e:
        current_app.logger.error(f'Error en dashboard: {str(e)}')
        flash('Error al cargar las estadísticas del dashboard', 'error')
        
        # Fallback a datos básicos
        total_contactos = Contacto.query.filter_by(user_id=current_user.id).count()
        ultimos_contactos = Contacto.query.filter_by(user_id=current_user.id)\
                                         .order_by(desc(Contacto.fecha_creacion))\
                                         .limit(5).all()
        total_interacciones = db.session.query(func.count(Interaccion.id))\
                                       .join(Contacto)\
                                       .filter(Contacto.user_id == current_user.id)\
                                       .scalar()
        
        grafico_etiquetas_fallback = generar_grafico_etiquetas_fallback(current_user.id)
        
        return render_template('dashboard.html', 
                             total_contactos=total_contactos,
                             ultimos_contactos=ultimos_contactos,
                             total_interacciones=total_interacciones,
                             grafico_etiquetas=grafico_etiquetas_fallback,
                             estadisticas=None,
                             grafico_etiquetas_img=None,
                             grafico_etiquetas_data=grafico_etiquetas_fallback,
                             grafico_interacciones_img=None,
                             grafico_empresas_img=None)

def generar_grafico_etiquetas_fallback(user_id):
    """Genera datos de distribución de etiquetas (versión simplificada de fallback)"""
    try:
        # Obtener todos los contactos del usuario
        contactos = Contacto.query.filter_by(user_id=user_id).all()
        
        # Contar etiquetas
        todas_etiquetas = []
        for contacto in contactos:
            if contacto.get_etiquetas_list():
                todas_etiquetas.extend(contacto.get_etiquetas_list())
        
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