from django.urls import path
from .views import (  UsuarioList, UsuarioDetail, VehiculoList, VehiculoDetail,ConductorList, ConductorDetail, RutaList, RutaDetail, CalificacionList, CalificacionDetail, RecuperarContrasenaView, RestablecerContrasenaView)
from rest_framework_simplejwt.views import (TokenView, TokenRefreshView,)

urlpatterns = [
    path('usuarios/', UsuarioList.as_view(), name='listar_usuarios'),
    path('usuarios/<int:pk>/', UsuarioDetail.as_view(), name='detalle_usuario'),

    path('vehiculos/', VehiculoList.as_view(), name='listar_vehiculos'),
    path('vehiculos/<int:pk>/', VehiculoDetail.as_view(), name='detalle_vehiculo'),

    path('conductores/', ConductorList.as_view(), name='listar_conductores'),
    path('conductores/<int:pk>/', ConductorDetail.as_view(), name='detalle_conductor'),

    path('rutas/', RutaList.as_view(), name='rutas-disponibles'),
    path('rutas/<int:pk>/', RutaDetail.as_view(), name='detalle_ruta'),

    path('calificaciones/', CalificacionList.as_view(), name='listar_calificaciones'),
    path('calificaciones/<int:pk>/', CalificacionDetail.as_view(), name='detalle_calificacion'),
    
    path('auth/recuperar-contrasena/', RecuperarContrasenaView.as_view(), name='recuperar-contrasena'),
    path('auth/restablecer-contrasena/', RestablecerContrasenaView.as_view(), name='restablecer-contrasena'),

    path('api/token/', TokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]