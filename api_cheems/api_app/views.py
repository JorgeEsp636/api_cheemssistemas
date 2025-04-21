from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion
from .serializers import (UsuarioSerializer,VehiculoSerializer, ConductorSerializer, RutaSerializer,CalificacionSerializer
)
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario
from .utils.token import generar_token, verificar_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class VehiculoList(generics.ListCreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class VehiculoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class ConductorList(generics.ListCreateAPIView):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer

class ConductorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer

class RutaList(generics.ListCreateAPIView):
    serializer_class = RutaSerializer

    def get_queryset(self):
        queryset = Ruta.objects.all().select_related('id_vehiculos')  # para optimizar
        origen = self.request.query_params.get('origen')
        destino = self.request.query_params.get('destino')

        if origen:
            queryset = queryset.filter(origen__icontains=origen)
        if destino:
            queryset = queryset.filter(destino__icontains=destino)

        return queryset

class RutaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class CalificacionList(generics.ListCreateAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario')
        ruta_id = self.request.query_params.get('ruta')
        if usuario_id:
            queryset = queryset.filter(id_usuario_id=usuario_id)
        if ruta_id:
            queryset = queryset.filter(id_ruta_id=ruta_id)
        return queryset

class CalificacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer

# Esta es la vista para que el usuario pueda recuperar contraseña
class RecuperarContrasenaView(APIView):
    def post(self, request):
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
    def post(self, request):
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