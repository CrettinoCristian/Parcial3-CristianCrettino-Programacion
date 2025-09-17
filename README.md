# Mini CRM Personal

Un sistema web simple y eficiente para gestionar contactos y sus interacciones, diseñado como CRM básico para uso local.

## 🎯 Características Principales

- **Gestión de Usuarios**: Registro, login/logout con autenticación segura
- **CRUD de Contactos**: Crear, leer, actualizar y eliminar contactos
- **Historial de Interacciones**: Registrar y consultar interacciones con contactos
- **Búsqueda y Filtros**: Buscar por nombre, empresa o etiquetas
- **Dashboard con Métricas**: Estadísticas y gráficos de distribución
- **Interfaz Moderna**: UI limpia y responsiva con Bootstrap

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask**: Framework web de Python
- **SQLAlchemy**: ORM para manejo de base de datos
- **Flask-Migrate**: Migraciones de base de datos
- **Flask-Login**: Sistema de autenticación
- **bcrypt**: Hash seguro de contraseñas
- **PostgreSQL**: Base de datos principal

### Frontend
- **HTML5 + Jinja2**: Templates dinámicos
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript ES6**: Funcionalidades interactivas
- **Bootstrap Icons**: Iconografía moderna

### Visualización
- **Matplotlib**: Generación de gráficos
- **Pandas**: Procesamiento de datos

## 📁 Estructura del Proyecto

```
mini_crm/
├── app.py                 # Punto de entrada Flask
├── config.py              # Configuración de la aplicación
├── init_db.py             # Script de inicialización de BD
├── requirements.txt       # Dependencias de Python
├── README.md              # Documentación del proyecto
├── models/
│   └── __init__.py        # Modelos SQLAlchemy
├── routes/
│   ├── auth.py            # Rutas de autenticación
│   ├── main.py            # Rutas principales y dashboard
│   ├── contactos.py       # CRUD de contactos
│   └── interacciones.py   # Gestión de interacciones
├── templates/
│   ├── base.html          # Template base
│   ├── index.html         # Página de inicio
│   ├── dashboard.html     # Dashboard principal
│   ├── auth/
│   │   ├── login.html     # Formulario de login
│   │   └── register.html  # Formulario de registro
│   ├── contactos/
│   │   ├── listar.html    # Lista de contactos
│   │   ├── form.html      # Formulario de contacto
│   │   └── ver.html       # Detalles del contacto
│   └── interacciones/
│       ├── listar.html    # Lista de interacciones
│       ├── form.html      # Formulario de interacción
│       ├── ver.html       # Detalles de interacción
│       └── recientes.html # Interacciones recientes
├── static/
│   ├── css/
│   │   └── style.css      # Estilos personalizados
│   ├── js/
│   │   └── main.js        # JavaScript principal
│   └── images/            # Imágenes y gráficos
└── migrations/            # Archivos de migraciones
```

## 🚀 Instalación y Configuración

### Prerrequisitos

1. **Python 3.8+** instalado
2. **PostgreSQL** instalado y ejecutándose
3. **Git** (opcional, para clonar el repositorio)

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si tienes git instalado
git clone <url-del-repositorio>
cd mini_crm

# O simplemente descomprime el archivo ZIP en una carpeta
```

### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos

1. **Crear la base de datos en PostgreSQL:**

```sql
-- Conectarse a PostgreSQL como superusuario
psql -U postgres

-- Crear la base de datos
CREATE DATABASE mini_crm;

-- Crear usuario (opcional)
CREATE USER crm_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE mini_crm TO crm_user;
```

2. **Configurar credenciales en `config.py`:**

```python
# Editar la línea de SQLALCHEMY_DATABASE_URI en config.py
SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:password@localhost:5432/mini_crm'
```

### Paso 5: Inicializar Base de Datos

```bash
# Verificar conexión a la base de datos
python init_db.py --check-only

# Inicializar tablas y migraciones
python init_db.py

# Opcional: Crear datos de ejemplo para pruebas
python init_db.py --sample-data
```

### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 👤 Uso de la Aplicación

### Primer Uso

1. **Registrar una cuenta**: Ve a `/auth/register` o haz clic en "Registrarse"
2. **Iniciar sesión**: Usa tus credenciales en `/auth/login`
3. **Explorar el dashboard**: Ve las métricas y acciones rápidas

### Si usaste datos de ejemplo:
- **Email**: demo@minicrm.com
- **Password**: demo123

### Funcionalidades Principales

#### Gestión de Contactos
- **Crear contacto**: Botón "Nuevo Contacto" en el dashboard o navbar
- **Ver contactos**: Lista paginada con búsqueda y filtros
- **Editar contacto**: Desde la vista de detalles o lista
- **Eliminar contacto**: Con confirmación de seguridad

#### Interacciones
- **Nueva interacción**: Desde el contacto o dashboard
- **Plantillas**: Usa plantillas predefinidas para diferentes tipos
- **Historial**: Ve todas las interacciones por contacto
- **Búsqueda**: Filtra interacciones por fecha

#### Dashboard
- **Métricas**: Total de contactos e interacciones
- **Gráfico**: Distribución de etiquetas en tiempo real
- **Accesos rápidos**: Enlaces a funciones principales

## 🔧 Configuración Avanzada

### Variables de Entorno

Puedes configurar la aplicación usando variables de entorno:

```bash
# Configuración de base de datos
export DATABASE_URL="postgresql://usuario:password@localhost:5432/mini_crm"

# Clave secreta para sesiones
export SECRET_KEY="tu-clave-secreta-muy-segura"

# Modo de desarrollo/producción
export FLASK_ENV="development"
```

### Configuración de Producción

Para uso en producción, modifica `config.py`:

```python
class ProductionConfig(Config):
    DEBUG = False
    # Usar variables de entorno para credenciales
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
```

## 🗃️ Estructura de Base de Datos

### Tabla `users`
- `id`: Clave primaria
- `nombre`: Nombre completo del usuario
- `email`: Email único para login
- `password_hash`: Contraseña hasheada con bcrypt
- `fecha_registro`: Timestamp de registro

### Tabla `contactos`
- `id`: Clave primaria
- `user_id`: FK a users
- `nombre`: Nombre del contacto (requerido)
- `email`: Email del contacto
- `telefono`: Teléfono del contacto
- `empresa`: Empresa del contacto
- `etiquetas`: Array de strings (PostgreSQL)
- `notas`: Texto libre para notas
- `ultima_interaccion`: Fecha de última interacción
- `fecha_creacion`: Timestamp de creación
- `fecha_actualizacion`: Timestamp de última actualización

### Tabla `interacciones`
- `id`: Clave primaria
- `contacto_id`: FK a contactos
- `fecha`: Fecha y hora de la interacción
- `nota`: Descripción de la interacción
- `fecha_creacion`: Timestamp de registro

## 🛡️ Seguridad

- **Autenticación**: Flask-Login con sesiones seguras
- **Contraseñas**: Hash con bcrypt y salt
- **Autorización**: Cada usuario ve solo sus datos
- **Validación**: Validación de formularios en frontend y backend
- **CSRF**: Protección contra ataques CSRF
- **SQL Injection**: Prevención con SQLAlchemy ORM

## 🐛 Solución de Problemas

### Error de Conexión a Base de Datos
```bash
# Verificar que PostgreSQL esté ejecutándose
sudo service postgresql status  # Linux
brew services list | grep postgresql  # macOS
# En Windows: Verificar en Servicios

# Verificar que la base de datos exista
psql -U postgres -l
```

### Error de Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error de Migraciones
```bash
# Eliminar carpeta migrations y reinicializar
rm -rf migrations/
python init_db.py
```

### Puerto en Uso
```bash
# Cambiar puerto en app.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Usar puerto 5001
```

## 📝 Desarrollo y Contribución

### Agregar Nuevas Funcionalidades

1. **Crear nueva ruta**: Agregar en `routes/`
2. **Crear template**: Agregar en `templates/`
3. **Actualizar modelos**: Modificar `models/__init__.py`
4. **Crear migración**: `flask db migrate -m "descripción"`
5. **Aplicar migración**: `flask db upgrade`

### Estructura de Commits
```
feat: agregar nueva funcionalidad
fix: corregir bug
docs: actualizar documentación
style: cambios de formato
refactor: refactorización de código
test: agregar pruebas
```

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Soporte

Si encuentras algún problema o tienes sugerencias:

1. Revisa la sección de "Solución de Problemas"
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que PostgreSQL esté ejecutándose
4. Revisa los logs de la aplicación para errores específicos

---

**Mini CRM Personal** - Sistema de gestión de contactos simple y eficiente para uso local.