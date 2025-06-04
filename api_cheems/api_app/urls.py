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

6. Zonas:
   - /zonas/ - Lista y creación de zonas
   - /zonas/<id>/ - Operaciones CRUD sobre una zona específica

7. Tarifas:
   - /tarifas/ - Lista y creación de tarifas
   - /tarifas/<id>/ - Operaciones CRUD sobre una tarifa específica
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UsuarioList, UsuarioDetail,
    VehiculoList, VehiculoDetail,
    ConductorList, ConductorDetail,
    RutaList, RutaDetail,
    CalificacionList, CalificacionDetail,
    RecuperarContrasenaView, RestablecerContrasenaView,
    CustomTokenObtainPairView, RolList, RolDetail,
    ZonaList, ZonaDetail, TarifaList, TarifaDetail,
    ImportarRutasView, DescargarPlantillaRutasView,
    ViajeList, ViajeDetail, RutaFavoritaList, RutaFavoritaDetail,
    CalificacionConductorList, CalificacionConductorDetail,
    DashboardEmpresaView, EstadisticaEmpresaView,
    VersionSistemaList, VersionSistemaDetail,
    PQRSList, PQRSDetail, PQRSAdminList
)

# Definición de las rutas URL de la API
urlpatterns = [
    # Rutas para usuarios
    path('usuarios/', UsuarioList.as_view(), name='usuario-list'),
    path('usuarios/<int:pk>/', UsuarioDetail.as_view(), name='usuario-detail'),
    
    # Rutas para roles
    path('roles/', RolList.as_view(), name='rol-list'),
    path('roles/<int:pk>/', RolDetail.as_view(), name='rol-detail'),
    
    # Rutas para zonas
    path('zonas/', ZonaList.as_view(), name='zona-list'),
    path('zonas/<int:pk>/', ZonaDetail.as_view(), name='zona-detail'),
    
    # Rutas para tarifas
    path('tarifas/', TarifaList.as_view(), name='tarifa-list'),
    path('tarifas/<int:pk>/', TarifaDetail.as_view(), name='tarifa-detail'),
    
    # Rutas para vehículos
    path('vehiculos/', VehiculoList.as_view(), name='vehiculo-list'),
    path('vehiculos/<int:pk>/', VehiculoDetail.as_view(), name='vehiculo-detail'),
    
    # Rutas para conductores
    path('conductores/', ConductorList.as_view(), name='conductor-list'),
    path('conductores/<int:pk>/', ConductorDetail.as_view(), name='conductor-detail'),
    
    # Rutas para rutas
    path('rutas/', RutaList.as_view(), name='ruta-list'),
    path('rutas/<int:pk>/', RutaDetail.as_view(), name='ruta-detail'),
    path('rutas/importar/', ImportarRutasView.as_view(), name='ruta-importar'),
    path('rutas/plantilla/', DescargarPlantillaRutasView.as_view(), name='ruta-plantilla'),
    
    # Rutas para calificaciones
    path('calificaciones/', CalificacionList.as_view(), name='calificacion-list'),
    path('calificaciones/<int:pk>/', CalificacionDetail.as_view(), name='calificacion-detail'),
    
    # Rutas para viajes
    path('viajes/', ViajeList.as_view(), name='viaje-list'),
    path('viajes/<int:pk>/', ViajeDetail.as_view(), name='viaje-detail'),
    
    # Rutas para rutas favoritas
    path('rutas-favoritas/', RutaFavoritaList.as_view(), name='ruta-favorita-list'),
    path('rutas-favoritas/<int:pk>/', RutaFavoritaDetail.as_view(), name='ruta-favorita-detail'),
    path('calificaciones-conductores/', CalificacionConductorList.as_view(), name='calificacion-conductor-list'),
    path('calificaciones-conductores/<int:pk>/', CalificacionConductorDetail.as_view(), name='calificacion-conductor-detail'),
    
    # Rutas para el dashboard de empresas
    path('dashboard/empresa/', DashboardEmpresaView.as_view(), name='dashboard-empresa'),
    path('estadisticas/empresa/', EstadisticaEmpresaView.as_view(), name='estadistica-empresa-list'),
    
    # Rutas para el control de versiones
    path('versiones/', VersionSistemaList.as_view(), name='version-sistema-list'),
    path('versiones/<int:pk>/', VersionSistemaDetail.as_view(), name='version-sistema-detail'),
    
    # Rutas para PQRS
    path('pqrs/', PQRSList.as_view(), name='pqrs-list'),
    path('pqrs/<int:pk>/', PQRSDetail.as_view(), name='pqrs-detail'),
    path('pqrs/admin/', PQRSAdminList.as_view(), name='pqrs-admin-list'),
    
    # Rutas para autenticación y recuperación de contraseña
    path('auth/recuperar-contrasena/', RecuperarContrasenaView.as_view(), name='recuperar-contrasena'),
    path('auth/restablecer-contrasena/', RestablecerContrasenaView.as_view(), name='restablecer-contrasena'),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]