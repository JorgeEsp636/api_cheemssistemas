"""
URLs de la aplicación api_app.

Este archivo define todas las rutas de la API REST, organizadas por funcionalidad:

1. Autenticación y Usuarios:
   - /usuarios/ - Lista y creación de usuarios
   - /usuarios/<id>/ - Operaciones CRUD sobre un usuario específico
   - /auth/recuperar-contrasena/ - Recuperación de contraseña
   - /auth/restablecer-contrasena/ - Restablecimiento de contraseña

2. Vehículos:
   - /vehiculos/ - Lista y creación de vehículos
   - /vehiculos/<id>/ - Operaciones CRUD sobre un vehículo específico

3. Conductores:
   - /conductores/ - Lista y creación de conductores
   - /conductores/<id>/ - Operaciones CRUD sobre un conductor específico

4. Rutas:
   - /rutas/ - Lista y creación de rutas
   - /rutas/<id>/ - Operaciones CRUD sobre una ruta específica

5. Calificaciones:
   - /calificaciones/ - Lista y creación de calificaciones
   - /calificaciones/<id>/ - Operaciones CRUD sobre una calificación específica
"""

from django.urls import path
from .views import (
    UsuarioList, UsuarioDetail,
    VehiculoList, VehiculoDetail,
    ConductorList, ConductorDetail,
    RutaList, RutaDetail,
    CalificacionList, CalificacionDetail,
    RecuperarContrasenaView, RestablecerContrasenaView,
    CustomTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView

# Definición de las rutas URL de la API
urlpatterns = [
    # Rutas para usuarios
    path('usuarios/', UsuarioList.as_view(), name='usuario-list'),
    path('usuarios/<int:pk>/', UsuarioDetail.as_view(), name='usuario-detail'),
    
    # Rutas para vehículos
    path('vehiculos/', VehiculoList.as_view(), name='vehiculo-list'),
    path('vehiculos/<int:pk>/', VehiculoDetail.as_view(), name='vehiculo-detail'),
    
    # Rutas para conductores
    path('conductores/', ConductorList.as_view(), name='conductor-list'),
    path('conductores/<int:pk>/', ConductorDetail.as_view(), name='conductor-detail'),
    
    # Rutas para rutas
    path('rutas/', RutaList.as_view(), name='ruta-list'),
    path('rutas/<int:pk>/', RutaDetail.as_view(), name='ruta-detail'),
    
    # Rutas para calificaciones
    path('calificaciones/', CalificacionList.as_view(), name='calificacion-list'),
    path('calificaciones/<int:pk>/', CalificacionDetail.as_view(), name='calificacion-detail'),
    
    # Rutas para autenticación y recuperación de contraseña
    path('auth/recuperar-contrasena/', RecuperarContrasenaView.as_view(), name='recuperar-contrasena'),
    path('auth/restablecer-contrasena/', RestablecerContrasenaView.as_view(), name='restablecer-contrasena'),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]