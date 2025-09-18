# Mini CRM Personal

Un sistema web simple y eficiente para gestionar contactos y sus interacciones, diseñado como CRM básico con despliegue en la nube.

## 🎯 Características Principales

- **Gestión de Usuarios**: Registro, login/logout con autenticación segura
- **CRUD de Contactos**: Crear, leer, actualizar y eliminar contactos
- **Historial de Interacciones**: Registrar y consultar interacciones con contactos
- **Búsqueda y Filtros**: Buscar por nombre, empresa o etiquetas
- **Dashboard con Métricas**: Estadísticas y gráficos de distribución
- **Interfaz Moderna**: UI limpia y responsiva con Bootstrap
- **Despliegue en la Nube**: Aplicación desplegada en Vercel con base de datos Neon

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask**: Framework web de Python
- **SQLAlchemy**: ORM para manejo de base de datos
- **Flask-Migrate**: Migraciones de base de datos
- **Flask-Login**: Sistema de autenticación
- **bcrypt**: Hash seguro de contraseñas
- **Neon PostgreSQL**: Base de datos en la nube

### Despliegue
- **Vercel**: Plataforma de despliegue
- **Neon**: Base de datos PostgreSQL serverless

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

### Opción 1: Desarrollo Local

#### Prerrequisitos
1. **Python 3.8+** instalado
2. **Git** (opcional, para clonar el repositorio)

#### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si tienes git instalado
git clone <url-del-repositorio>
cd mini_crm

# O simplemente descomprime el archivo ZIP en una carpeta
```

#### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

#### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### Paso 4: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Base de datos Neon PostgreSQL
DATABASE_URL=postgresql://neondb_owner:tu_password@ep-flat-resonance-ad2muymd-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require

# Clave secreta para sesiones
SECRET_KEY=tu-clave-secreta-muy-segura

# Modo de desarrollo
FLASK_ENV=development
```

#### Paso 5: Inicializar Base de Datos

```bash
# Inicializar tablas en Neon
python init_vercel_db.py
```

#### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

### Opción 2: Despliegue en Vercel

La aplicación está configurada para desplegarse automáticamente en Vercel:

1. **Fork o clona** este repositorio
2. **Conecta tu repositorio** a Vercel
3. **Configura las variables de entorno** en Vercel:
   - `DATABASE_URL`: URL de conexión a Neon PostgreSQL
   - `SECRET_KEY`: Clave secreta para sesiones
4. **Despliega** automáticamente

#### Variables de Entorno en Vercel

```
DATABASE_URL=postgresql://neondb_owner:password@host.neon.tech/neondb?sslmode=require
SECRET_KEY=tu-clave-secreta-muy-segura
```

La aplicación estará disponible en: **http://localhost:5000**

## 👤 Uso de la Aplicación

### Primer Uso

1. **Registrar una cuenta**: Ve a `/auth/register` o haz clic en "Registrarse"
2. **Iniciar sesión**: Usa tus credenciales en `/auth/login`
3. **Explorar el dashboard**: Ve las métricas y acciones rápidas

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

La aplicación utiliza las siguientes variables de entorno:

```bash
# Base de datos Neon PostgreSQL
DATABASE_URL="postgresql://neondb_owner:password@host.neon.tech/neondb?sslmode=require"

# Clave secreta para sesiones
SECRET_KEY="tu-clave-secreta-muy-segura"

# Modo de desarrollo/producción
FLASK_ENV="development"
```

### Configuración de Producción

Para despliegue en producción (Vercel), la aplicación automáticamente:
- Detecta las variables de entorno configuradas en Vercel
- Usa Neon PostgreSQL como base de datos
- Configura el modo de producción automáticamente

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

### Error de Conexión a Base de Datos Neon
```bash
# Verificar que la URL de Neon sea correcta
# Asegurarse de que incluya ?sslmode=require
DATABASE_URL=postgresql://neondb_owner:password@host.neon.tech/neondb?sslmode=require

# Verificar que las credenciales sean válidas en Neon Console
```

### Error de Variables de Entorno
```bash
# Verificar que el archivo .env existe y tiene las variables correctas
cat .env

# En Vercel, verificar que las variables estén configuradas en el dashboard
```

### Error de Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error de Inicialización de Base de Datos
```bash
# Ejecutar el script de inicialización para Neon
python init_vercel_db.py
```

### Puerto en Uso (Desarrollo Local)
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
3. Asegúrate de que las variables de entorno estén configuradas correctamente
4. Para problemas con Neon PostgreSQL, verifica la conexión en Neon Console
5. Para problemas con Vercel, revisa los logs de despliegue en el dashboard
6. Revisa los logs de la aplicación para errores específicos

### Enlaces Útiles

- **Aplicación en Vercel**: [URL de tu aplicación desplegada]
- **Neon Console**: https://console.neon.tech
- **Vercel Dashboard**: https://vercel.com/dashboard

---

**Mini CRM Personal** - Sistema de gestión de contactos con despliegue en la nube usando Vercel y Neon PostgreSQL.