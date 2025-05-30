# API Cheems Sistemas

API REST para el sistema de gestión de rutas de transporte.

## Requisitos Previos

- Python 3.8 o superior
- PostgreSQL
- pip (gestor de paquetes de Python)

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
```

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
python manage.py runserver
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

## Características Especiales

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

Ejecutar las pruebas:
```bash
python manage.py test
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