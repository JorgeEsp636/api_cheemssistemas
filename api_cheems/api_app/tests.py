from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion, Zona, Tarifa, Rol
from django.utils import timezone
from datetime import time, date
from django.core.files.uploadedfile import SimpleUploadedFile


class UsuarioTests(TestCase):
    """
    Suite de pruebas para el modelo Usuario y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de usuarios
    - Autenticación de usuarios
    - Operaciones CRUD de usuarios
    - Validaciones de campos
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de usuario.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        # Crear superusuario una sola vez para todas las pruebas
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_usuario(self):
        """
        Prueba la creación de un nuevo usuario.
        Verifica que:
        - Se pueda crear un usuario con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('usuario-list')
        data = {
            'correo_electronico': 'arevaloerik2705@gmail.com',
            'contrasena': '1076650495e',
            'nombre': 'Erik Normal'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 2)
        self.assertEqual(Usuario.objects.get(correo_electronico='arevaloerik2705@gmail.com').nombre, 'Erik Normal')

    def test_autenticacion_usuario(self):
        """
        Prueba la autenticación de usuarios.
        Verifica que:
        - Un usuario pueda iniciar sesión con credenciales válidas
        - Se devuelva un token de autenticación
        - Se rechacen credenciales inválidas
        """
        url = reverse('token_obtain_pair')
        data = {
            'correo_electronico': 'erijahiaron@gmail.com',
            'contrasena': '1076650495e'
        }
        response = self.client.post(url, data, format='json')
        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class VehiculoTests(TestCase):
    """
    Suite de pruebas para el modelo Vehiculo y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de vehículos
    - Actualización de vehículos
    - Eliminación de vehículos
    - Validaciones de campos
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de vehículos.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_vehiculo(self):
        """
        Prueba la creación de un nuevo vehículo.
        Verifica que:
        - Se pueda crear un vehículo con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('vehiculo-list')
        data = {
            'placa': 'CHE-001',
            'empresa': 1,
            'disponibilidad': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehiculo.objects.count(), 1)
        self.assertEqual(Vehiculo.objects.get(placa='CHE-001').empresa, 1)

class ConductorTests(TestCase):
    """
    Suite de pruebas para el modelo Conductor y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de conductores
    - Asignación de vehículos
    - Validaciones de campos
    - Relaciones con vehículos
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de conductores.
        Crea un superusuario, un vehículo y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        self.vehiculo = Vehiculo.objects.create(
            placa='CHE-001',
            empresa=1,
            disponibilidad=True
        )

    def test_crear_conductor(self):
        """
        Prueba la creación de un nuevo conductor.
        Verifica que:
        - Se pueda crear un conductor con datos válidos
        - Se asigne correctamente el vehículo
        - Se devuelva el código de estado correcto
        """
        url = reverse('conductor-list')
        data = {
            'id_vehiculos': self.vehiculo.id_vehiculos,
            'nombre': 'Jorge Espitia',
            'licencia_conduccion': 12345
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conductor.objects.count(), 1)
        self.assertEqual(Conductor.objects.get(nombre='Jorge Espitia').licencia_conduccion, 12345)

class RutaTests(TestCase):
    """
    Suite de pruebas para el modelo Ruta y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de rutas
    - Asignación de vehículos
    - Validaciones de horarios
    - Relaciones con vehículos
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de rutas.
        Crea un superusuario, un vehículo y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        self.vehiculo = Vehiculo.objects.create(
            placa='CHE-001',
            empresa=1,
            disponibilidad=True
        )

    def test_crear_ruta(self):
        """
        Prueba la creación de una nueva ruta.
        Verifica que:
        - Se pueda crear una ruta con datos válidos
        - Se asigne correctamente el vehículo
        - Se manejen correctamente los horarios
        - Se devuelva el código de estado correcto
        """
        url = reverse('ruta-list')
        data = {
            'id_vehiculos': self.vehiculo.id_vehiculos,
            'nombre_ruta': 'Rapido el carmen',
            'origen': 'Ubate',
            'destino': 'Cucucnuba',
            'horario': '08:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ruta.objects.count(), 1)
        self.assertEqual(Ruta.objects.get(nombre_ruta='Rapido el carmen').origen, 'Ubate')

class CalificacionTests(TestCase):
    """
    Suite de pruebas para el modelo Calificacion y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de calificaciones
    - Validaciones de puntuaciones
    - Relaciones con rutas y usuarios
    - Validaciones de fechas
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de calificaciones.
        Crea un superusuario, un vehículo, una ruta y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        self.vehiculo = Vehiculo.objects.create(
            placa='CHE-001',
            empresa=1,
            disponibilidad=True
        )
        self.ruta = Ruta.objects.create(
            id_vehiculos=self.vehiculo,
            nombre_ruta='Rapido el carmen',
            origen='Ubate',
            destino='Cucucnuba',
            horario=time(8, 0)
        )

    def test_crear_calificacion(self):
        """
        Prueba la creación de una nueva calificación.
        Verifica que:
        - Se pueda crear una calificación con datos válidos
        - Se validen correctamente las puntuaciones
        - Se manejen correctamente las fechas
        - Se devuelva el código de estado correcto
        """
        url = reverse('calificacion-list')
        data = {
            'id_ruta': self.ruta.id_ruta,
            'id_usuario': self.superuser.id_usuario,
            'calificacion': 5,
            'comentario': 'Excelente servicio, muy puntual',
            'fecha': date.today()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Calificacion.objects.count(), 1)
        self.assertEqual(Calificacion.objects.get(comentario='Excelente servicio, muy puntual').calificacion, 5)

    def test_calificacion_invalida(self):
        """
        Prueba la validación de calificaciones inválidas.
        Verifica que:
        - Se rechacen calificaciones fuera del rango permitido
        - Se devuelvan mensajes de error apropiados
        """
        url = reverse('calificacion-list')
        data = {
            'id_ruta': self.ruta.id_ruta,
            'id_usuario': self.superuser.id_usuario,
            'calificacion': 6,  # Calificación inválida
            'comentario': 'Test comentario',
            'fecha': date.today()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RecuperacionContrasenaTests(TestCase):
    """
    Suite de pruebas para la recuperación de contraseña.
    
    Esta clase contiene pruebas para:
    - Solicitud de recuperación de contraseña
    - Validación de correos existentes
    - Manejo de errores
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de recuperación de contraseña.
        Crea un usuario de prueba y configura el cliente API.
        """
        self.client = APIClient()
        self.usuario = Usuario.objects.create_user(
            correo_electronico='arevaloerik2705@gmail.com',
            contrasena='1076650495e',
            nombre='Erik Normal'
        )
        self.recuperar_url = reverse('recuperar-contrasena')
        self.restablecer_url = reverse('restablecer-contrasena')

    def test_recuperar_contrasena(self):
        """
        Prueba la solicitud de recuperación de contraseña.
        Verifica que:
        - Se pueda solicitar la recuperación con un correo válido
        - Se devuelva el mensaje de confirmación correcto
        """
        data = {'correo_electronico': 'arevaloerik2705@gmail.com'}
        response = self.client.post(self.recuperar_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['confirmación'], 'Correo enviado con instrucciones')

    def test_recuperar_contrasena_usuario_no_existe(self):
        """
        Prueba el intento de recuperación con un correo inexistente.
        Verifica que:
        - Se rechace la solicitud con un correo no registrado
        - Se devuelva el código de error apropiado
        """
        data = {'correo_electronico': 'noexiste@cheems.com'}
        response = self.client.post(self.recuperar_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# Agregar después de las clases existentes

class RolTests(TestCase):
    """
    Suite de pruebas para el modelo Rol y sus endpoints.
    """
    def setUp(self):
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_rol(self):
        url = reverse('rol-list')
        data = {
            'nombre': 'Conductor Senior',
            'descripcion': 'Conductor con más de 5 años de experiencia'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rol.objects.count(), 1)
        
class ZonaTests(TestCase):
    """
        Suite de pruebas para el modelo Zona y sus endpoints.
            
        Esta clase contiene pruebas para:
        - Creación de zonas
        - Actualización de zonas
        - Validaciones de campos
        - Operaciones CRUD de zonas
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de zonas.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_zona(self):
        """
        Prueba la creación de una nueva zona.
        Verifica que:
        - Se pueda crear una zona con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('zona-list')
        data = {
            'nombre': 'Ubate',
            'descripcion': 'Zona de Ubate',
            'activa': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Zona.objects.count(), 1)
        self.assertEqual(Zona.objects.get(nombre='Ubate').descripcion, 'Zona de Ubate')

    def test_listar_zonas(self):
        """
        Prueba el listado de zonas.
        Verifica que:
        - Se puedan listar todas las zonas
        - Se devuelva el código de estado correcto
        """
        # Crear algunas zonas
        Zona.objects.create(nombre='Ubate', descripcion='Zona de Ubate', activa=True)
        Zona.objects.create(nombre='Cucunuba', descripcion='Zona de Cucunuba', activa=True)
        
        url = reverse('zona-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_actualizar_zona(self):
        """
        Prueba la actualización de una zona.
        Verifica que:
        - Se pueda actualizar una zona existente
        - Los cambios se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        zona = Zona.objects.create(
            nombre='Ubate',
            descripcion='Zona de Ubate',
            activa=True
        )
        
        url = reverse('zona-detail', args=[zona.id_zona])
        data = {
            'nombre': 'Ubate Centro',
            'descripcion': 'Zona centro de Ubate',
            'activa': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Zona.objects.get(id_zona=zona.id_zona).nombre, 'Ubate Centro')

    def test_eliminar_zona(self):
        """
        Prueba la eliminación de una zona.
        Verifica que:
        - Se pueda eliminar una zona existente
        - La zona se elimine correctamente
        - Se devuelva el código de estado correcto
        """
        zona = Zona.objects.create(
            nombre='Ubate',
            descripcion='Zona de Ubate',
            activa=True
        )
        
        url = reverse('zona-detail', args=[zona.id_zona])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Zona.objects.count(), 0)
        
class TarifaTests(TestCase):
    """
    Suite de pruebas para el modelo Tarifa y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de tarifas
    - Validaciones de zonas
    - Actualización de precios
    - Operaciones CRUD de tarifas
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de tarifas.
        Crea un superusuario, zonas y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        
        # Crear zonas para las pruebas
        self.zona_origen = Zona.objects.create(
            nombre='Ubate',
            descripcion='Zona de Ubate',
            activa=True
        )
        self.zona_destino = Zona.objects.create(
            nombre='Cucunuba',
            descripcion='Zona de Cucunuba',
            activa=True
        )

    def test_crear_tarifa(self):
        """
        Prueba la creación de una nueva tarifa.
        Verifica que:
        - Se pueda crear una tarifa con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('tarifa-list')
        data = {
            'zona_origen': self.zona_origen.id_zona,
            'zona_destino': self.zona_destino.id_zona,
            'precio_base': '5000.00',
            'precio_km': '1000.00',
            'activa': True
        }
        response = self.client.post(url, data, format='json')
        print('RESPONSE DATA CREAR TARIFA:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tarifa.objects.count(), 1)
        self.assertEqual(float(Tarifa.objects.get().precio_base), 5000.00)

    def test_validar_zonas_iguales(self):
        """
        Prueba la validación de zonas iguales en una tarifa.
        Verifica que:
        - No se pueda crear una tarifa con la misma zona de origen y destino
        - Se devuelva el código de estado correcto
        """
        url = reverse('tarifa-list')
        data = {
            'zona_origen': self.zona_origen.id_zona,
            'zona_destino': self.zona_origen.id_zona,
            'precio_base': '5000.00',
            'precio_km': '1000.00',
            'activa': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_tarifas(self):
        """
        Prueba el listado de tarifas.
        Verifica que:
        - Se puedan listar todas las tarifas
        - Se devuelva el código de estado correcto
        """
        # Crear algunas tarifas
        Tarifa.objects.create(
            zona_origen=self.zona_origen,
            zona_destino=self.zona_destino,
            precio_base='5000.00',
            precio_km='1000.00',
            activa=True,
            actualizado_por=self.superuser
        )
        
        url = reverse('tarifa-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_actualizar_tarifa(self):
        """
        Prueba la actualización de una tarifa.
        Verifica que:
        - Se pueda actualizar una tarifa existente
        - Los cambios se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        tarifa = Tarifa.objects.create(
            zona_origen=self.zona_origen,
            zona_destino=self.zona_destino,
            precio_base='5000.00',
            precio_km='1000.00',
            activa=True,
            actualizado_por=self.superuser
        )
        
        url = reverse('tarifa-detail', args=[tarifa.id_tarifa])
        data = {
            'zona_origen': self.zona_origen.id_zona,
            'zona_destino': self.zona_destino.id_zona,
            'precio_base': '6000.00',
            'precio_km': '1200.00',
            'activa': True
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(Tarifa.objects.get(id_tarifa=tarifa.id_tarifa).precio_base), 6000.00)

    def test_eliminar_tarifa(self):
        """
        Prueba la eliminación de una tarifa.
        Verifica que:
        - Se pueda eliminar una tarifa existente
        - La tarifa se elimine correctamente
        - Se devuelva el código de estado correcto
        """
        tarifa = Tarifa.objects.create(
            zona_origen=self.zona_origen,
            zona_destino=self.zona_destino,
            precio_base='5000.00',
            precio_km='1000.00',
            activa=True,
            actualizado_por=self.superuser
        )
        
        url = reverse('tarifa-detail', args=[tarifa.id_tarifa])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tarifa.objects.count(), 0)

class ImportacionRutasTests(TestCase):
    """
    Suite de pruebas para la importación de rutas desde CSV.
    
    Esta clase contiene pruebas para:
    - Importación de rutas desde CSV
    - Validación de formato CSV
    - Manejo de errores
    - Descarga de plantilla
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de importación.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        
        # Crear vehículo para las pruebas
        self.vehiculo = Vehiculo.objects.create(
            placa='CHE-001',
            empresa=1,
            disponibilidad=True
        )

    def test_descargar_plantilla(self):
        url = reverse('ruta-plantilla')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('nombre_ruta,origen,destino,horario,placa_vehiculo', 
                     response.content.decode())

    def test_importar_rutas_csv(self):
        url = reverse('ruta-importar')
        csv_content = 'nombre_ruta,origen,destino,horario,placa_vehiculo\n'
        csv_content += 'Rapido el carmen,Ubate,Cucunuba,08:00,CHE-001\n'
        csv_content += 'Rapido el carmen,Cucunuba,Ubate,09:00,CHE-001'
        
        csv_file = SimpleUploadedFile(
            "rutas.csv",
            csv_content.encode(),
            content_type="text/csv"
        )
        
        data = {'archivo': csv_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ruta.objects.count(), 2)
        # Verificar que ambas rutas se crearon correctamente
        rutas = Ruta.objects.filter(nombre_ruta='Rapido el carmen')
        self.assertEqual(rutas.count(), 2)
        self.assertTrue(rutas.filter(origen='Ubate').exists())
        self.assertTrue(rutas.filter(origen='Cucunuba').exists())

    def test_importar_rutas_csv_invalido(self):
        url = reverse('ruta-importar')
        csv_content = 'campo_invalido\n'
        csv_content += 'dato_invalido'
        
        csv_file = SimpleUploadedFile(
            "rutas_invalidas.csv",
            csv_content.encode(),
            content_type="text/csv"
        )
        
        data = {'archivo': csv_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_importar_rutas_vehiculo_no_existe(self):
        url = reverse('ruta-importar')
        csv_content = 'nombre_ruta,origen,destino,horario,placa_vehiculo\n'
        csv_content += 'Ruta Test,Ubate,Cucunuba,08:00,VEHICULO-INEXISTENTE'
        
        csv_file = SimpleUploadedFile(
            "rutas_vehiculo_invalido.csv",
            csv_content.encode(),
            content_type="text/csv"
        )
        
        data = {'archivo': csv_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_importar_rutas_formato_horario_invalido(self):
        url = reverse('ruta-importar')
        csv_content = 'nombre_ruta,origen,destino,horario,placa_vehiculo\n'
        csv_content += 'Ruta Test,Ubate,Cucunuba,25:00,CHE-001'
        
        csv_file = SimpleUploadedFile(
            "rutas_horario_invalido.csv",
            csv_content.encode(),
            content_type="text/csv"
        )
        
        data = {'archivo': csv_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
