# Configuración de Vercel Postgres

## Pasos para configurar Vercel Postgres

### 1. Crear base de datos en Vercel
1. Ve a tu dashboard de Vercel
2. Selecciona tu proyecto
3. Ve a la pestaña "Storage"
4. Haz clic en "Create Database"
5. Selecciona "Postgres"
6. Elige un nombre para tu base de datos
7. Selecciona la región más cercana
8. Haz clic en "Create"

### 2. Conectar la base de datos al proyecto
1. Una vez creada la base de datos, haz clic en "Connect Project"
2. Selecciona tu proyecto Flask
3. Vercel automáticamente configurará las variables de entorno necesarias

### 3. Variables de entorno automáticas
Vercel configurará automáticamente estas variables:
- `POSTGRES_URL` - URL completa de conexión
- `POSTGRES_PRISMA_URL` - URL con connection pooling
- `POSTGRES_URL_NON_POOLING` - URL sin connection pooling
- `POSTGRES_USER` - Usuario de la base de datos
- `POSTGRES_HOST` - Host de la base de datos
- `POSTGRES_PASSWORD` - Contraseña
- `POSTGRES_DATABASE` - Nombre de la base de datos

### 4. Configuración en el código
El código ya está configurado para usar estas variables automáticamente:
- En `config.py`, la configuración de producción usa `POSTGRES_URL` o `DATABASE_URL`
- Si no encuentra estas variables, usa SQLite como fallback

### 5. Migración de datos
Para migrar datos existentes:
1. Exporta los datos de tu base de datos actual
2. Usa las herramientas de Vercel o conecta directamente a la base de datos Postgres
3. Importa los datos usando SQL o scripts de migración

### 6. Despliegue
1. Haz commit de todos los cambios
2. Push al repositorio
3. Vercel automáticamente desplegará con la nueva configuración de base de datos

## Comandos útiles

### Conectar a la base de datos localmente (opcional)
```bash
# Instalar psql si no lo tienes
# En Windows: descargar PostgreSQL
# En macOS: brew install postgresql
# En Linux: sudo apt-get install postgresql-client

# Conectar usando la URL de Vercel
psql $POSTGRES_URL
```

### Verificar conexión en Python
```python
import os
import psycopg2

# Usar la URL de Vercel
conn = psycopg2.connect(os.environ['POSTGRES_URL'])
cur = conn.cursor()
cur.execute('SELECT version()')
print(cur.fetchone())
conn.close()
```

## Notas importantes
- Las variables de entorno se configuran automáticamente en Vercel
- No necesitas configurar nada manualmente en las variables de entorno de Vercel
- La base de datos es persistente, a diferencia de SQLite en Vercel
- Vercel Postgres incluye connection pooling automático
- Los datos se mantienen entre despliegues