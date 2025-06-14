# API Cheems Sistemas

API REST para el sistema de gestión de rutas de transporte.

## Requisitos Previos

- Python 3.8 o superior
- PostgreSQL
- pip (gestor de paquetes de Python)
- OpenSSL (para certificados SSL/TLS)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd api_cheems
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar base de datos:
- Crear una base de datos PostgreSQL llamada `apicheemsdb`
- Configurar las credenciales en `api_cheems/settings.py` si es necesario

5. Aplicar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

## Configuración

### Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
SECRET_KEY=tu_clave_secreta
DEBUG=True
DB_NAME=apicheemsdb
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://tudominio.com
```

### Configuración de Seguridad
La API implementa varias capas de seguridad:

1. **Autenticación y Autorización**
   - JWT (JSON Web Tokens) para autenticación
   - Tokens de acceso con expiración de 1 hora
   - Tokens de actualización con expiración de 1 día
   - Protección contra ataques de fuerza bruta
   - Límite de intentos de inicio de sesión

2. **Protección de Datos**
   - Encriptación de contraseñas con bcrypt
   - Protección contra ataques XSS y CSRF
   - Validación de datos de entrada
   - Sanitización de datos sensibles

3. **Seguridad de la API**
   - Rate limiting por IP y usuario
   - Protección contra ataques de inyección SQL
   - Headers de seguridad configurados
   - Validación de origen de peticiones (CORS)

4. **Monitoreo y Logging**
   - Registro de intentos de inicio de sesión
   - Detección de actividades sospechosas
   - Logs de seguridad centralizados
   - Alertas de seguridad configurables

### Configuración de Correo
En `settings.py`, configurar las credenciales de correo para el envío de tokens:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_correo@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña'
```

## Uso

### Iniciar el Servidor
```bash
# Desarrollo
python manage.py runserver

# Producción con SSL
python manage.py runsslserver --certificate /ruta/a/certificado.crt --key /ruta/a/llave.key
```

### Endpoints Principales

#### Autenticación
- `POST /api/token/`: Obtener token de acceso
  - Body: `{"correo_electronico": "usuario@ejemplo.com", "contrasena": "contraseña"}`
- `POST /api/token/refresh/`: Renovar token de acceso
  - Body: `{"refresh": "token_de_actualización"}`

#### Usuarios
- `GET /usuarios/`: Listar usuarios
- `POST /usuarios/`: Crear usuario
- `GET /usuarios/{id}/`: Obtener usuario
- `PUT /usuarios/{id}/`: Actualizar usuario
- `DELETE /usuarios/{id}/`: Eliminar usuario

#### Vehículos
- `GET /vehiculos/`: Listar vehículos
- `POST /vehiculos/`: Crear vehículo
- `GET /vehiculos/{id}/`: Obtener vehículo
- `PUT /vehiculos/{id}/`: Actualizar vehículo
- `DELETE /vehiculos/{id}/`: Eliminar vehículo

#### Conductores
- `GET /conductores/`: Listar conductores
- `POST /conductores/`: Crear conductor
- `GET /conductores/{id}/`: Obtener conductor
- `PUT /conductores/{id}/`: Actualizar conductor
- `DELETE /conductores/{id}/`: Eliminar conductor

#### Rutas
- `GET /rutas/`: Listar rutas
- `POST /rutas/`: Crear ruta
- `GET /rutas/{id}/`: Obtener ruta
- `PUT /rutas/{id}/`: Actualizar ruta
- `DELETE /rutas/{id}/`: Eliminar ruta

#### Calificaciones
- `GET /calificaciones/`: Listar calificaciones
- `POST /calificaciones/`: Crear calificación
- `GET /calificaciones/{id}/`: Obtener calificación
- `PUT /calificaciones/{id}/`: Actualizar calificación
- `DELETE /calificaciones/{id}/`: Eliminar calificación

#### Zonas
- `GET /zonas/`: Listar zonas
- `POST /zonas/`: Crear zona
- `GET /zonas/{id}/`: Obtener zona
- `PUT /zonas/{id}/`: Actualizar zona
- `DELETE /zonas/{id}/`: Eliminar zona

#### Tarifas
- `GET /tarifas/`: Listar tarifas
- `POST /tarifas/`: Crear tarifa
- `GET /tarifas/{id}/`: Obtener tarifa
- `PUT /tarifas/{id}/`: Actualizar tarifa
- `DELETE /tarifas/{id}/`: Eliminar tarifa

### Importación de Rutas
- `GET /rutas/plantilla/`: Descargar plantilla CSV para importación
- `POST /rutas/importar/`: Importar rutas desde archivo CSV
  - Formato CSV requerido: nombre_ruta,origen,destino,horario,placa_vehiculo
  - Validaciones automáticas de formato y datos

### Gestión de Tarifas
- Validación automática de zonas origen y destino
- Precios base y por kilómetro configurables
- Control de tarifas activas/inactivas
- Registro de actualizaciones por usuario

## Características Especiales

### Seguridad Avanzada
- Protección contra ataques de fuerza bruta
- Límite de intentos de inicio de sesión
- Detección de actividades sospechosas
- Registro de eventos de seguridad
- Protección contra ataques XSS y CSRF
- Validación de datos de entrada
- Sanitización de datos sensibles

### Autenticación Personalizada
- Usa correo electrónico en lugar de username
- Implementa JWT para tokens de acceso
- Tokens de acceso válidos por 1 hora
- Tokens de actualización válidos por 1 día

### Recuperación de Contraseña
- Envío de correo con token de recuperación
- Token válido por 1 hora
- Restablecimiento seguro de contraseña

### Filtros
- Rutas: filtrado por origen y destino
- Calificaciones: filtrado por usuario y ruta

## Pruebas

El proyecto incluye una suite completa de pruebas automatizadas que cubre:

- Autenticación y gestión de usuarios
- CRUD de vehículos y conductores
- Gestión de rutas y calificaciones
- Importación de rutas desde CSV
- Gestión de zonas y tarifas
- Validaciones de datos y reglas de negocio
- Pruebas de seguridad y protección
- Pruebas de rate limiting y protección contra ataques

Para ejecutar las pruebas:
```bash
python manage.py test
```

Para ejecutar pruebas específicas:
```bash
python manage.py test api_app.tests.UsuarioTests
python manage.py test api_app.tests.TarifaTests
python manage.py test api_app.tests.ImportacionRutasTests
python manage.py test api_app.tests.SecurityTests
```

## Estructura del Proyecto

```
api_cheems/
├── api_app/
│   ├── migrations/
│   ├── utils/
│   │   └── token.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── api_cheems/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
└── manage.py
```

## Notas Importantes

1. **Autenticación**:
   - Todos los endpoints requieren autenticación excepto `/api/token/` y `/api/token/refresh/`
   - Usar el token en el header: `Authorization: Bearer <token>`

2. **Base de Datos**:
   - Usar PostgreSQL como motor de base de datos
   - Las credenciales se configuran en `settings.py`

3. **Seguridad**:
   - No exponer el archivo `.env` en el repositorio
   - Mantener las claves secretas seguras
   - Usar HTTPS en producción

## Contribución

1. Crear una rama para la nueva característica
2. Realizar los cambios necesarios
3. Ejecutar las pruebas
4. Crear un pull request