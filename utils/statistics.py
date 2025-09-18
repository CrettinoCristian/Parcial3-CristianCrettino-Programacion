"""
Utilidades para generar estadísticas y gráficos del CRM
"""
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para servidor
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from datetime import datetime, timedelta
from flask import current_app
from models import Contacto, Interaccion, db
from sqlalchemy import func, extract

# Configuración de matplotlib para mejor apariencia
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#212529',
    'axes.facecolor': '#343a40',
    'axes.edgecolor': '#6c757d',
    'axes.labelcolor': '#ffffff',
    'text.color': '#ffffff',
    'xtick.color': '#ffffff',
    'ytick.color': '#ffffff',
    'grid.color': '#495057',
    'grid.alpha': 0.3
})

def generar_grafico_etiquetas(user_id):
    """
    Genera un gráfico de barras con la distribución de etiquetas
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
        
        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        etiquetas = [item[0] for item in etiquetas_top]
        valores = [item[1] for item in etiquetas_top]
        
        # Colores atractivos
        colores = ['#0d6efd', '#198754', '#dc3545', '#ffc107', '#6f42c1', 
                  '#fd7e14', '#20c997', '#e83e8c', '#6c757d', '#17a2b8']
        
        bars = ax.bar(etiquetas, valores, color=colores[:len(etiquetas)])
        
        # Personalización
        ax.set_title('Distribución de Etiquetas de Contactos', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Etiquetas', fontsize=12)
        ax.set_ylabel('Cantidad de Contactos', fontsize=12)
        
        # Rotar etiquetas si son muchas
        if len(etiquetas) > 5:
            plt.xticks(rotation=45, ha='right')
        
        # Agregar valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{valor}', ha='center', va='bottom', fontweight='bold')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Convertir a base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='#212529', edgecolor='none')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64, dict(contador.most_common(10))
        
    except Exception as e:
        current_app.logger.error(f'Error generando gráfico de etiquetas: {str(e)}')
        return None, None

def generar_grafico_interacciones_tiempo(user_id):
    """
    Genera un gráfico de líneas mostrando interacciones por mes
    """
    try:
        # Obtener interacciones de los últimos 12 meses
        fecha_limite = datetime.now() - timedelta(days=365)
        
        interacciones = db.session.query(
            extract('year', Interaccion.fecha).label('año'),
            extract('month', Interaccion.fecha).label('mes'),
            func.count(Interaccion.id).label('total')
        ).join(Contacto).filter(
            Contacto.user_id == user_id,
            Interaccion.fecha >= fecha_limite
        ).group_by('año', 'mes').order_by('año', 'mes').all()
        
        if not interacciones:
            return None
        
        # Preparar datos
        meses = []
        totales = []
        
        for interaccion in interacciones:
            mes_nombre = datetime(int(interaccion.año), int(interaccion.mes), 1).strftime('%b %Y')
            meses.append(mes_nombre)
            totales.append(interaccion.total)
        
        # Crear gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(meses, totales, marker='o', linewidth=3, markersize=8, 
               color='#0d6efd', markerfacecolor='#ffffff', markeredgecolor='#0d6efd')
        
        # Personalización
        ax.set_title('Interacciones por Mes', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Mes', fontsize=12)
        ax.set_ylabel('Número de Interacciones', fontsize=12)
        
        # Rotar etiquetas del eje X
        plt.xticks(rotation=45, ha='right')
        
        # Grid
        ax.grid(True, alpha=0.3)
        
        # Rellenar área bajo la curva
        ax.fill_between(meses, totales, alpha=0.3, color='#0d6efd')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Convertir a base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight',
                   facecolor='#212529', edgecolor='none')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
        
    except Exception as e:
        current_app.logger.error(f'Error generando gráfico de interacciones: {str(e)}')
        return None

def generar_grafico_contactos_empresa(user_id):
    """
    Genera un gráfico de dona mostrando distribución por empresa
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
        
        # Crear gráfico de dona
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = [item[0] for item in top_empresas]
        sizes = [item[1] for item in top_empresas]
        
        # Colores atractivos
        colores = ['#0d6efd', '#198754', '#dc3545', '#ffc107', '#6f42c1', 
                  '#fd7e14', '#20c997', '#e83e8c', '#6c757d']
        
        # Crear dona
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                         colors=colores, startangle=90,
                                         wedgeprops=dict(width=0.5))
        
        # Personalizar texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title('Distribución de Contactos por Empresa', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Ajustar layout
        plt.tight_layout()
        
        # Convertir a base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight',
                   facecolor='#212529', edgecolor='none')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_base64
        
    except Exception as e:
        current_app.logger.error(f'Error generando gráfico de empresas: {str(e)}')
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