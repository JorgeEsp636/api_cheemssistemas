from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion
from .serializers import (UsuarioSerializer,VehiculoSerializer, ConductorSerializer, RutaSerializer,CalificacionSerializer
)

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
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vehiculo_id = self.request.query_params.get('vehiculo')
        if vehiculo_id:
            queryset = queryset.filter(id_vehiculos_id=vehiculo_id)
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
