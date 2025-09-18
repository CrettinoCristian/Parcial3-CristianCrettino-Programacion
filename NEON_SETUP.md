# 🐘 Configuración de Neon PostgreSQL (RECOMENDADO)

## ¿Por qué Neon?
- ✅ **3GB gratuitos** (más que Railway)
- ✅ PostgreSQL serverless
- ✅ Muy rápido
- ✅ Interfaz moderna
- ✅ Branching de base de datos
- ✅ No requiere tarjeta de crédito

## Paso 1: Crear cuenta
1. Ve a https://neon.tech
2. Regístrate con GitHub (recomendado)
3. Verifica tu email

## Paso 2: Crear proyecto
1. Click "Create Project"
2. Nombre: `parcial3-crettino`
3. Región: `US East (Ohio)` (más rápida)
4. PostgreSQL version: 15 (default)
5. Click "Create Project"

## Paso 3: Obtener connection string
1. En el dashboard, ve a "Connection Details"
2. Copia la **Connection string**
3. Se ve así: `postgresql://usuario:password@host/database?sslmode=require`

## Paso 4: Configurar tu aplicación

### Opción A: Archivo .env local
```env
DATABASE_URL=postgresql://usuario:password@host/database?sslmode=require
POSTGRES_URL=postgresql://usuario:password@host/database?sslmode=require
```

### Opción B: Variables de entorno en Vercel
1. Ve a tu proyecto en Vercel
2. Settings > Environment Variables
3. Agrega:
   - `DATABASE_URL` = tu connection string
   - `POSTGRES_URL` = tu connection string

## Paso 5: Inicializar base de datos
Ejecuta tu script de inicialización:
```bash
python init_vercel_db.py
```

## Ventajas adicionales:
- 🔄 Branching: puedes crear copias de tu DB para testing
- 📊 Query insights y métricas
- 🔒 SSL por defecto
- ⚡ Autoscaling automático
- 🌐 CDN global