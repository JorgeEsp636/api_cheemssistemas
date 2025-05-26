from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion
from .serializers import (UsuarioSerializer,VehiculoSerializer, ConductorSerializer, RutaSerializer,CalificacionSerializer, CustomTokenObtainPairSerializer)
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario
from .utils.token import generar_token, verificar_token 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

class UsuarioList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de usuarios y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todos los usuarios registrados
    - POST: Crear un nuevo usuario
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre un usuario específico.
    
    Esta vista permite:
    - GET: Obtener los detalles de un usuario específico
    - PUT/PATCH: Actualizar los datos de un usuario
    - DELETE: Eliminar un usuario
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

class VehiculoList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de vehículos y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todos los vehículos registrados
    - POST: Crear un nuevo vehículo
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

class VehiculoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre un vehículo específico.
    
    Esta vista permite:
    - GET: Obtener los detalles de un vehículo específico
    - PUT/PATCH: Actualizar los datos de un vehículo
    - DELETE: Eliminar un vehículo
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

class ConductorList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de conductores y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todos los conductores registrados
    - POST: Crear un nuevo conductor
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [IsAuthenticated]

class ConductorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre un conductor específico.
    
    Esta vista permite:
    - GET: Obtener los detalles de un conductor específico
    - PUT/PATCH: Actualizar los datos de un conductor
    - DELETE: Eliminar un conductor
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [IsAuthenticated]

class RutaList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de rutas y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todas las rutas registradas
    - POST: Crear una nueva ruta
    
    Características especiales:
    - Permite filtrar rutas por origen y destino
    - Utiliza select_related para optimizar las consultas a la base de datos
    """
    serializer_class = RutaSerializer

    def get_queryset(self):
        """
        Método para obtener y filtrar las rutas.
        
        Filtros disponibles:
        - origen: Filtra rutas que contengan el texto especificado en el origen
        - destino: Filtra rutas que contengan el texto especificado en el destino
        
        Returns:
            QuerySet: Conjunto de rutas filtradas según los parámetros
        """
        queryset = Ruta.objects.all().select_related('id_vehiculos') 
        origen = self.request.query_params.get('origen')
        destino = self.request.query_params.get('destino')

        if origen:
            queryset = queryset.filter(origen__icontains=origen)
        if destino:
            queryset = queryset.filter(destino__icontains=destino)

        return queryset

class RutaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una ruta específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una ruta específica
    - PUT/PATCH: Actualizar los datos de una ruta
    - DELETE: Eliminar una ruta
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [IsAuthenticated]

class CalificacionList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de calificaciones y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todas las calificaciones registradas
    - POST: Crear una nueva calificación
    
    Características especiales:
    - Permite filtrar calificaciones por usuario y ruta
    - Requiere autenticación para acceder
    """
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener y filtrar las calificaciones.
        
        Filtros disponibles:
        - usuario: Filtra calificaciones por ID de usuario
        - ruta: Filtra calificaciones por ID de ruta
        
        Returns:
            QuerySet: Conjunto de calificaciones filtradas según los parámetros
        """
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario')
        ruta_id = self.request.query_params.get('ruta')
        if usuario_id:
            queryset = queryset.filter(id_usuario_id=usuario_id)
        if ruta_id:
            queryset = queryset.filter(id_ruta_id=ruta_id)
        return queryset

class CalificacionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una calificación específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una calificación específica
    - PUT/PATCH: Actualizar los datos de una calificación
    - DELETE: Eliminar una calificación
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

# Esta es la vista para que el usuario pueda recuperar contraseña
class RecuperarContrasenaView(APIView):
    """
    Vista para manejar la recuperación de contraseña de usuarios.
    
    Esta vista permite:
    - POST: Solicitar la recuperación de contraseña
    
    Proceso:
    1. Recibe el correo electrónico del usuario
    2. Genera un token único
    3. Envía un correo con el enlace para restablecer la contraseña
    
    Respuestas:
    - 200: Correo enviado exitosamente
    - 404: Usuario no encontrado
    """
    def post(self, request):
        """
        Método para procesar la solicitud de recuperación de contraseña.
        
        Args:
            request: Objeto Request con el correo electrónico del usuario
            
        Returns:
            Response: Respuesta con el estado de la operación
        """
        email = request.data.get('correo_electronico')
        try:
            usuario = Usuario.objects.get(correo_electronico=email)
            token = generar_token(email)
            link = f"http://localhost:8000/api/auth/restablecer-contrasena/?token={token}"
            send_mail(
                subject="Recupera tu contraseña",
                message=f"Haz clic en el siguiente enlace para restablecer tu contraseña: {link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )
            return Response({'confirmación': 'Correo enviado con instrucciones'}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Esta es la vista para que el usuario pueda restablecer la contraseña
class RestablecerContrasenaView(APIView):
    """
    Vista para manejar el restablecimiento de contraseña.
    
    Esta vista permite:
    - POST: Restablecer la contraseña usando el token recibido
    
    Proceso:
    1. Verifica el token recibido
    2. Actualiza la contraseña del usuario
    3. Confirma la actualización
    
    Respuestas:
    - 200: Contraseña actualizada exitosamente
    - 400: Token inválido o expirado
    - 404: Usuario no encontrado
    """
    def post(self, request):
        """
        Método para procesar el restablecimiento de contraseña.
        
        Args:
            request: Objeto Request con la nueva contraseña y el token
            
        Returns:
            Response: Respuesta con el estado de la operación
        """
        token = request.query_params.get('token')
        nueva_contrasena = request.data.get('nueva_contrasena')

        email = verificar_token(token)
        if email:
            try:
                usuario = Usuario.objects.get(correo_electronico=email)
                usuario.contrasena = make_password(nueva_contrasena)
                usuario.save()
                return Response({'confirmación': 'Su contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
            except Usuario.DoesNotExist:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para la autenticación.
    
    Usa el serializer CustomTokenObtainPairSerializer para autenticar con correo_electronico y contrasena.
    """
    serializer_class = CustomTokenObtainPairSerializer