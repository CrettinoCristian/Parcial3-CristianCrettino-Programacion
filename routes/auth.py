from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from urllib.parse import urlparse
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta de inicio de sesión"""
    if request.method == 'POST':
        try:
            print("[DEBUG VERCEL] Iniciando proceso de login")
            email = request.form.get('email')
            password = request.form.get('password')
            
            print(f"[DEBUG VERCEL] Email recibido: {email}")
            print(f"[DEBUG VERCEL] Password length: {len(password) if password else 0}")
            
            if not email or not password:
                print("[DEBUG VERCEL] Email o password faltante")
                flash('Por favor, completa todos los campos.', 'error')
                return render_template('auth/login.html')
            
            print("[DEBUG VERCEL] Buscando usuario en base de datos")
            user = User.query.filter_by(email=email).first()
            
            if not user:
                print(f"[DEBUG VERCEL] Usuario no encontrado: {email}")
                flash('Credenciales inválidas.', 'error')
                return render_template('auth/login.html')
            
            print(f"[DEBUG VERCEL] Usuario encontrado: {user.nombre}")
            print(f"[DEBUG VERCEL] Verificando contraseña...")
            
            if user.check_password(password):
                print("[DEBUG VERCEL] Contraseña correcta, iniciando sesión")
                login_user(user, remember=request.form.get('remember'))
                next_page = request.args.get('next')
                print(f"[DEBUG VERCEL] Redirigiendo a: {next_page or '/dashboard'}")
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            else:
                print("[DEBUG VERCEL] Contraseña incorrecta")
                flash('Credenciales inválidas.', 'error')
                return render_template('auth/login.html')
                
        except Exception as e:
            print(f"[DEBUG VERCEL] Error en login: {str(e)}")
            print(f"[DEBUG VERCEL] Error type: {type(e).__name__}")
            import traceback
            print(f"[DEBUG VERCEL] Traceback: {traceback.format_exc()}")
            flash('Error de conexión. Inténtalo de nuevo.', 'error')
            return render_template('auth/login.html')
    
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
        try:
            if os.environ.get('FLASK_ENV') == 'production':
                print(f"[DEBUG] Checking if email exists: {email}")
            
            existing_user = User.query.filter_by(email=email).first()
            
            if os.environ.get('FLASK_ENV') == 'production':
                print(f"[DEBUG] Email exists: {'Yes' if existing_user else 'No'}")
            
            if existing_user:
                flash('Este email ya está registrado.', 'error')
                return render_template('auth/register.html')
        except Exception as e:
            if os.environ.get('FLASK_ENV') == 'production':
                print(f"[DEBUG] Error checking existing user: {str(e)}")
            flash('Error de conexión. Inténtalo de nuevo.', 'error')
            return render_template('auth/register.html')
        
        # Crear nuevo usuario
        try:
            # Debug logging para producción
            if os.environ.get('FLASK_ENV') == 'production':
                print(f"[DEBUG] Attempting to create user: {email}")
            
            user = User(nombre=nombre, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            if os.environ.get('FLASK_ENV') == 'production':
                print(f"[DEBUG] User created successfully: {user.id}")
            
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            if os.environ.get('FLASK_ENV') == 'production':
                print(f"[DEBUG] Error creating user: {str(e)}")
            flash('Error al crear la cuenta. Inténtalo de nuevo.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))