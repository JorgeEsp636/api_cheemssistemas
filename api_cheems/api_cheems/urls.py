"""
URL configuration for api_cheems project.

Este archivo define las rutas URL principales del proyecto.
Las rutas están organizadas de la siguiente manera:

1. /admin/ - Panel de administración de Django
2. /api/ - Endpoints de la API REST
3. /swagger/ - Documentación interactiva de la API (Swagger UI)
4. /redoc/ - Documentación alternativa de la API (ReDoc)
"""

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Endpoints de la API REST
    path('api/', include('api_app.urls')),
]
