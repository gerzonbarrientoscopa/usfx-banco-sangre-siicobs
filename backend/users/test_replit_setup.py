"""Comprobaciones del acceso real para la instalación de prueba."""
import secrets

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class ReplitAccessTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = secrets.token_urlsafe(24)
        self.user = User.objects.create_superuser(
            username='prueba_arranque', password=self.password
        )

    def test_rechaza_credenciales_incorrectas(self):
        response = self.client.post('/api/v1/user/login', {
            'username': self.user.username,
            'password': 'incorrecta',
        })
        self.assertEqual(response.status_code, 400)

    def test_acceso_informacion_y_cierre_de_sesion(self):
        response = self.client.post('/api/v1/user/login', {
            'username': self.user.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 200)
        token = response.data['data']['x_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.get('/api/v1/user/info')
        self.assertEqual(response.status_code, 200)
        self.assertIn('admin', response.data['data']['roles'])

        response = self.client.post('/api/v1/graphql/', {
            'query': '{ __typename }',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('errors', response.json())

        response = self.client.post('/api/v1/user/logout')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Token.objects.filter(user=self.user).exists())
