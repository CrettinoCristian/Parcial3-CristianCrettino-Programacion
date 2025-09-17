from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, Contacto, Interaccion
from sqlalchemy import or_, desc
from datetime import datetime

contactos_bp = Blueprint('contactos', __name__, url_prefix='/contactos')

@contactos_bp.route('/')
@login_required
def listar():
    """Lista todos los contactos del usuario con búsqueda y filtros"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    etiqueta_filter = request.args.get('etiqueta', '')
    
    # Query base
    query = Contacto.query.filter_by(user_id=current_user.id)
    
    # Aplicar búsqueda
    if search:
        query = query.filter(
            or_(
                Contacto.nombre.ilike(f'%{search}%'),
                Contacto.email.ilike(f'%{search}%'),
                Contacto.empresa.ilike(f'%{search}%')
            )
        )
    
    # Aplicar filtro por etiqueta
    if etiqueta_filter:
        # Buscar contactos que contengan la etiqueta en su campo JSON
        query = query.filter(Contacto.etiquetas.like(f'%"{etiqueta_filter}"%'))
    
    # Ordenar por última interacción
    contactos = query.order_by(desc(Contacto.ultima_interaccion)).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Obtener todas las etiquetas únicas para el filtro
    todas_etiquetas = set()
    for contacto in Contacto.query.filter_by(user_id=current_user.id).all():
        if contacto.etiquetas_list:
            todas_etiquetas.update(contacto.etiquetas_list)
    
    return render_template('contactos/listar.html', 
                         contactos=contactos,
                         search=search,
                         etiqueta_filter=etiqueta_filter,
                         todas_etiquetas=sorted(todas_etiquetas))

@contactos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    """Crear un nuevo contacto"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        empresa = request.form.get('empresa')
        etiquetas_str = request.form.get('etiquetas')
        notas = request.form.get('notas')
        
        # Validaciones
        if not nombre:
            flash('El nombre es obligatorio.', 'error')
            return render_template('contactos/form.html')
        
        # Verificar email único para el usuario
        if email:
            contacto_existente = Contacto.query.filter_by(
                user_id=current_user.id, email=email
            ).first()
            if contacto_existente:
                flash('Ya tienes un contacto con este email.', 'error')
                return render_template('contactos/form.html')
        
        try:
            # Crear nuevo contacto
            contacto = Contacto(
                user_id=current_user.id,
                nombre=nombre,
                email=email,
                telefono=telefono,
                empresa=empresa,
                notas=notas
            )
            
            # Procesar etiquetas
            contacto.set_etiquetas_from_str(etiquetas_str)
            
            db.session.add(contacto)
            db.session.commit()
            
            flash(f'Contacto "{nombre}" creado exitosamente.', 'success')
            return redirect(url_for('contactos.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el contacto. Inténtalo de nuevo.', 'error')
    
    return render_template('contactos/form.html')

@contactos_bp.route('/<int:id>')
@login_required
def ver(id):
    """Ver detalles de un contacto"""
    contacto = Contacto.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Obtener últimas interacciones
    interacciones = Interaccion.query.filter_by(contacto_id=contacto.id).order_by(desc(Interaccion.fecha)).limit(5).all()
    
    return render_template('contactos/ver.html', 
                         contacto=contacto, 
                         interacciones=interacciones)

@contactos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar un contacto existente"""
    contacto = Contacto.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        empresa = request.form.get('empresa')
        etiquetas_str = request.form.get('etiquetas')
        notas = request.form.get('notas')
        
        # Validaciones
        if not nombre:
            flash('El nombre es obligatorio.', 'error')
            return render_template('contactos/form.html', contacto=contacto)
        
        # Verificar email único (excluyendo el contacto actual)
        if email:
            contacto_existente = Contacto.query.filter(
                Contacto.user_id == current_user.id,
                Contacto.email == email,
                Contacto.id != id
            ).first()
            if contacto_existente:
                flash('Ya tienes otro contacto con este email.', 'error')
                return render_template('contactos/form.html', contacto=contacto)
        
        try:
            # Actualizar contacto
            contacto.nombre = nombre
            contacto.email = email
            contacto.telefono = telefono
            contacto.empresa = empresa
            contacto.notas = notas
            contacto.set_etiquetas_from_str(etiquetas_str)
            contacto.fecha_actualizacion = datetime.utcnow()
            
            db.session.commit()
            
            flash(f'Contacto "{nombre}" actualizado exitosamente.', 'success')
            return redirect(url_for('contactos.ver', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el contacto. Inténtalo de nuevo.', 'error')
    
    return render_template('contactos/form.html', contacto=contacto)

@contactos_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    """Eliminar un contacto"""
    contacto = Contacto.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        nombre = contacto.nombre
        db.session.delete(contacto)
        db.session.commit()
        
        flash(f'Contacto "{nombre}" eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el contacto.', 'error')
    
    return redirect(url_for('contactos.listar'))

@contactos_bp.route('/api/etiquetas')
@login_required
def api_etiquetas():
    """API para obtener todas las etiquetas del usuario (para autocompletado)"""
    etiquetas = set()
    contactos = Contacto.query.filter_by(user_id=current_user.id).all()
    
    for contacto in contactos:
        if contacto.etiquetas_list:
            etiquetas.update(contacto.etiquetas_list)
    
    return jsonify(sorted(list(etiquetas)))