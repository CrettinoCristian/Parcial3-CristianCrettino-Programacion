from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from urllib.parse import urlparse
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        # Debug logging para producción
        if os.environ.get('FLASK_ENV') == 'production':
            print(f"[DEBUG] Login attempt for email: {email}")
            print(f"[DEBUG] Password provided: {'Yes' if password else 'No'}")
        
        if not email or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('auth/login.html')
        
        try:
            user = User.query.filter_by(email=email).first()
            
            if os.environ.get('FLASK_ENV') == 'production':
                print(f"[DEBUG] User found: {'Yes' if user else 'No'}")
                if user:
                    print(f"[DEBUG] User ID: {user.id}, Name: {user.nombre}")
            
            if user and user.check_password(password):
                if os.environ.get('FLASK_ENV') == 'production':
                    print(f"[DEBUG] Password check: Success")
                
                login_user(user, remember=remember)
                next_page = request.args.get('next')
                if not next_page or urlparse(next_page).netloc != '':
                    next_page = url_for('main.dashboard')
                flash(f'¡Bienvenido {user.nombre}!', 'success')
                return redirect(next_page)
            else:
                if os.environ.get('FLASK_ENV') == 'production':
                    print(f"[DEBUG] Password check: Failed")
                flash('Email o contraseña incorrectos.', 'error')
                
        except Exception as e:
            if os.environ.get('FLASK_ENV') == 'production':
                print(f"[DEBUG] Database error during login: {str(e)}")
            flash('Error de conexión. Inténtalo de nuevo.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de usuario"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones
        if not all([nombre, email, password, confirm_password]):
            flash('Por favor completa todos los campos.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('auth/register.html')
        
        # Verificar si el email ya existe
        if User.query.filter_by(email=email).first():
            flash('Este email ya está registrado.', 'error')
            return render_template('auth/register.html')
        
        # Crear nuevo usuario
        try:
            user = User(nombre=nombre, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la cuenta. Inténtalo de nuevo.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))