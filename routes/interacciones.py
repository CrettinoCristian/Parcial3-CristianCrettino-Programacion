from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, Contacto, Interaccion
from sqlalchemy import desc
from datetime import datetime

interacciones_bp = Blueprint('interacciones', __name__, url_prefix='/interacciones')

@interacciones_bp.route('/contacto/<int:contacto_id>')
@login_required
def listar(contacto_id):
    """Lista todas las interacciones de un contacto"""
    contacto = Contacto.query.filter_by(id=contacto_id, user_id=current_user.id).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    interacciones = Interaccion.query.filter_by(contacto_id=contacto_id)\
                                   .order_by(desc(Interaccion.fecha))\
                                   .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('interacciones/listar.html', 
                         contacto=contacto, 
                         interacciones=interacciones)

@interacciones_bp.route('/contacto/<int:contacto_id>/nueva', methods=['GET', 'POST'])
@login_required
def nueva(contacto_id):
    """Crear una nueva interacción para un contacto"""
    contacto = Contacto.query.filter_by(id=contacto_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        nota = request.form.get('nota')
        
        # Validaciones
        if not nota:
            flash('La nota es obligatoria.', 'error')
            return render_template('interacciones/form.html', contacto=contacto)
        
        # Procesar fecha
        try:
            if fecha_str:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            else:
                fecha = datetime.utcnow()
        except ValueError:
            flash('Formato de fecha inválido.', 'error')
            return render_template('interacciones/form.html', contacto=contacto)
        
        try:
            # Crear nueva interacción
            interaccion = Interaccion(
                contacto_id=contacto_id,
                fecha=fecha,
                nota=nota
            )
            
            db.session.add(interaccion)
            
            # Actualizar última interacción del contacto
            contacto.actualizar_ultima_interaccion()
            
            db.session.commit()
            
            flash('Interacción agregada exitosamente.', 'success')
            return redirect(url_for('interacciones.listar', contacto_id=contacto_id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la interacción. Inténtalo de nuevo.', 'error')
    
    return render_template('interacciones/form.html', contacto=contacto)

@interacciones_bp.route('/<int:id>')
@login_required
def ver(id):
    """Ver detalles de una interacción"""
    interaccion = Interaccion.query.join(Contacto)\
                                 .filter(Interaccion.id == id,
                                        Contacto.user_id == current_user.id)\
                                 .first_or_404()
    
    return render_template('interacciones/ver.html', interaccion=interaccion)

@interacciones_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar una interacción existente"""
    interaccion = Interaccion.query.join(Contacto)\
                                 .filter(Interaccion.id == id,
                                        Contacto.user_id == current_user.id)\
                                 .first_or_404()
    
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        nota = request.form.get('nota')
        
        # Validaciones
        if not nota:
            flash('La nota es obligatoria.', 'error')
            return render_template('interacciones/form.html', 
                                 contacto=interaccion.contacto, 
                                 interaccion=interaccion)
        
        # Procesar fecha
        try:
            if fecha_str:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')
            else:
                fecha = interaccion.fecha
        except ValueError:
            flash('Formato de fecha inválido.', 'error')
            return render_template('interacciones/form.html', 
                                 contacto=interaccion.contacto, 
                                 interaccion=interaccion)
        
        try:
            # Actualizar interacción
            interaccion.fecha = fecha
            interaccion.nota = nota
            
            db.session.commit()
            
            flash('Interacción actualizada exitosamente.', 'success')
            return redirect(url_for('interacciones.ver', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar la interacción. Inténtalo de nuevo.', 'error')
    
    return render_template('interacciones/form.html', 
                         contacto=interaccion.contacto, 
                         interaccion=interaccion)

@interacciones_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    """Eliminar una interacción"""
    interaccion = Interaccion.query.join(Contacto)\
                                 .filter(Interaccion.id == id,
                                        Contacto.user_id == current_user.id)\
                                 .first_or_404()
    
    contacto_id = interaccion.contacto_id
    
    try:
        db.session.delete(interaccion)
        db.session.commit()
        
        flash('Interacción eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la interacción.', 'error')
    
    return redirect(url_for('interacciones.listar', contacto_id=contacto_id))

@interacciones_bp.route('/recientes')
@login_required
def recientes():
    """Ver las interacciones más recientes del usuario"""
    page = request.args.get('page', 1, type=int)
    
    interacciones = db.session.query(Interaccion)\
                             .join(Contacto)\
                             .filter(Contacto.user_id == current_user.id)\
                             .order_by(desc(Interaccion.fecha))\
                             .paginate(page=page, per_page=15, error_out=False)
    
    return render_template('interacciones/recientes.html', interacciones=interacciones)