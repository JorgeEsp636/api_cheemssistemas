from django.test import TestCase
from .models import Usuario, Vehiculo

class TestUsuario(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='erijahiaron@gmail.com',
            password='1076650495'
        )

    def test_usuario_creado_correctamente(self):
        self.assertEqual(self.usuario.username, 'testuser')
        self.assertEqual(self.usuario.email, 'erijahiaron@gmail.com')
        self.assertTrue(self.usuario.check_password('1076650495'))

class TestVehiculo(TestCase):
    def setUp(self):
        self.vehiculo = Vehiculo.objects.create(
            placa='ABC123',
            empresa=1,
            disponibilidad=True
        )

    def test_vehiculo_creado_correctamente(self):
        self.assertEqual(self.vehiculo.placa, 'ABC123')
        self.assertEqual(self.vehiculo.empresa, 1)
        self.assertTrue(self.vehiculo.disponibilidad)

    def test_vehiculo_str(self):
        self.assertEqual(str(self.vehiculo), 'ABC123')
