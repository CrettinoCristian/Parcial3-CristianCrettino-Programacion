# 🚀 Instrucciones Rápidas - Mini CRM Personal

## ⚡ Inicio Rápido

### 1. Verificar Prerrequisitos
- ✅ Python 3.8+ instalado
- ✅ PostgreSQL instalado y ejecutándose
- ✅ Todas las dependencias instaladas

### 2. Configurar Base de Datos

```sql
-- En PostgreSQL (como superusuario)
psql -U postgres
CREATE DATABASE mini_crm;
\q
```

### 3. Configurar Credenciales

Editar `config.py` línea 12:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://tu_usuario:tu_password@localhost:5432/mini_crm'
```

### 4. Inicializar Proyecto

```bash
# Instalar dependencias (ya hecho)
pip install -r requirements.txt

# Inicializar base de datos
python init_db.py --sample-data

# Ejecutar aplicación
python run.py --debug
```

### 5. Acceder a la Aplicación

🌐 **URL**: http://localhost:5000

**Datos de prueba** (si usaste --sample-data):
- 📧 **Email**: demo@minicrm.com
- 🔑 **Password**: demo123

---

## 📋 Comandos Útiles

```bash
# Ejecutar en modo desarrollo
python run.py --debug

# Ejecutar en puerto diferente
python run.py --port 8000

# Solo verificar conexión BD
python init_db.py --check-only

# Reinicializar BD con datos de ejemplo
python init_db.py --sample-data
```

---

## 🔧 Solución Rápida de Problemas

### Error de Conexión a BD
```bash
# Verificar PostgreSQL
psql -U postgres -c "SELECT version();"

# Verificar base de datos
psql -U postgres -l | grep mini_crm
```

### Error de Dependencias
```bash
pip install -r requirements.txt --force-reinstall
```

### Puerto en Uso
```bash
python run.py --port 5001
```

---

## 📱 Funcionalidades Principales

1. **👤 Registro/Login**: Crear cuenta y autenticarse
2. **📇 Gestión de Contactos**: CRUD completo con búsqueda
3. **💬 Interacciones**: Historial de comunicaciones
4. **📊 Dashboard**: Métricas y gráficos en tiempo real
5. **🏷️ Etiquetas**: Organización por categorías
6. **🔍 Búsqueda**: Filtros avanzados por múltiples criterios

---

## 📞 Soporte

Si tienes problemas:
1. Revisa el archivo `README.md` completo
2. Verifica que PostgreSQL esté ejecutándose
3. Confirma que las credenciales en `config.py` sean correctas
4. Revisa los logs en la terminal para errores específicos

---

**¡Listo para usar tu Mini CRM Personal! 🎉**