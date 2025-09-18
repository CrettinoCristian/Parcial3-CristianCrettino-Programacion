"""
Utilidades para generar estadísticas del CRM (versión optimizada para Vercel)
"""
from collections import Counter
from datetime import datetime, timedelta
from flask import current_app
from models import Contacto, Interaccion, db
from sqlalchemy import func, extract

def generar_grafico_etiquetas(user_id):
    """
    Genera datos de distribución de etiquetas (versión simplificada)
    """
    try:
        # Obtener contactos del usuario
        contactos = Contacto.query.filter_by(user_id=user_id).all()
        
        # Recopilar todas las etiquetas
        todas_etiquetas = []
        for contacto in contactos:
            if contacto.get_etiquetas_list():
                todas_etiquetas.extend(contacto.get_etiquetas_list())
        
        if not todas_etiquetas:
            return None, None
        
        # Contar frecuencias
        contador = Counter(todas_etiquetas)
        etiquetas_top = contador.most_common(10)
        
        if not etiquetas_top:
            return None, None
        
        # Retornar solo los datos, sin gráfico
        return None, dict(etiquetas_top)
        
    except Exception as e:
        current_app.logger.error(f'Error generando datos de etiquetas: {str(e)}')
        return None, None

def generar_grafico_interacciones_tiempo(user_id):
    """
    Genera datos de interacciones en el tiempo (versión simplificada)
    """
    try:
        # Obtener interacciones de los últimos 30 días
        fecha_limite = datetime.now() - timedelta(days=30)
        
        interacciones = db.session.query(
            func.date(Interaccion.fecha).label('fecha'),
            func.count(Interaccion.id).label('cantidad')
        ).join(Contacto)\
         .filter(Contacto.user_id == user_id)\
         .filter(Interaccion.fecha >= fecha_limite)\
         .group_by(func.date(Interaccion.fecha))\
         .order_by(func.date(Interaccion.fecha))\
         .all()
        
        if not interacciones:
            return None
        
        # Retornar datos básicos en lugar de gráfico
        datos = {
            'total_interacciones': sum(item.cantidad for item in interacciones),
            'dias_activos': len(interacciones),
            'promedio_diario': round(sum(item.cantidad for item in interacciones) / len(interacciones), 1)
        }
        
        return datos
        
    except Exception as e:
        current_app.logger.error(f'Error generando datos de interacciones: {str(e)}')
        return None

def generar_grafico_contactos_empresa(user_id):
    """
    Genera datos de distribución por empresa (versión simplificada)
    """
    try:
        # Obtener contactos agrupados por empresa
        contactos = Contacto.query.filter_by(user_id=user_id).all()
        
        empresas = {}
        sin_empresa = 0
        
        for contacto in contactos:
            if contacto.empresa and contacto.empresa.strip():
                empresa = contacto.empresa.strip()
                empresas[empresa] = empresas.get(empresa, 0) + 1
            else:
                sin_empresa += 1
        
        if not empresas and sin_empresa == 0:
            return None
        
        # Preparar datos (top 8 empresas + otros)
        empresas_ordenadas = sorted(empresas.items(), key=lambda x: x[1], reverse=True)
        
        if len(empresas_ordenadas) > 8:
            top_empresas = empresas_ordenadas[:7]
            otros_total = sum(count for _, count in empresas_ordenadas[7:])
            top_empresas.append(('Otras empresas', otros_total))
        else:
            top_empresas = empresas_ordenadas
        
        if sin_empresa > 0:
            top_empresas.append(('Sin empresa', sin_empresa))
        
        # Retornar datos en lugar de gráfico
        return dict(top_empresas)
        
    except Exception as e:
        current_app.logger.error(f'Error generando datos de empresas: {str(e)}')
        return None

def obtener_estadisticas_generales(user_id):
    """
    Obtiene estadísticas generales del usuario
    """
    try:
        # Estadísticas básicas
        total_contactos = Contacto.query.filter_by(user_id=user_id).count()
        
        total_interacciones = db.session.query(func.count(Interaccion.id))\
                                       .join(Contacto)\
                                       .filter(Contacto.user_id == user_id)\
                                       .scalar()
        
        # Contactos agregados este mes
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        contactos_mes = Contacto.query.filter(
            Contacto.user_id == user_id,
            Contacto.fecha_creacion >= inicio_mes
        ).count()
        
        # Interacciones este mes
        interacciones_mes = db.session.query(func.count(Interaccion.id))\
                                     .join(Contacto)\
                                     .filter(
                                         Contacto.user_id == user_id,
                                         Interaccion.fecha >= inicio_mes
                                     ).scalar()
        
        # Promedio de interacciones por contacto
        promedio_interacciones = round(total_interacciones / total_contactos, 1) if total_contactos > 0 else 0
        
        # Top 3 etiquetas
        contactos = Contacto.query.filter_by(user_id=user_id).all()
        todas_etiquetas = []
        for contacto in contactos:
            if contacto.get_etiquetas_list():
                todas_etiquetas.extend(contacto.get_etiquetas_list())
        
        top_etiquetas = Counter(todas_etiquetas).most_common(3) if todas_etiquetas else []
        
        return {
            'total_contactos': total_contactos,
            'total_interacciones': total_interacciones,
            'contactos_mes': contactos_mes,
            'interacciones_mes': interacciones_mes,
            'promedio_interacciones': promedio_interacciones,
            'top_etiquetas': top_etiquetas
        }
        
    except Exception as e:
        current_app.logger.error(f'Error obteniendo estadísticas generales: {str(e)}')
        return {
            'total_contactos': 0,
            'total_interacciones': 0,
            'contactos_mes': 0,
            'interacciones_mes': 0,
            'promedio_interacciones': 0,
            'top_etiquetas': []
        }