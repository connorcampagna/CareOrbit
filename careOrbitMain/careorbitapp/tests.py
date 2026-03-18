from django.test import TestCase
from django.contrib.auth.hashers import make_password
from careorbitapp.models import User


class AuthenticationTests(TestCase):

    def setUp(self):
        User.objects.create(
            name='Test User',
            email='test@test.com',
            passwordHash=make_password('password123'),
            nhsNumber='1234567890',
            date_of_birth='1990-01-01',
            phoneNumber='07700000000',
            role='patient',
        )

    def test_login_page_loads(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_correct_credentials(self):
        response = self.client.post('/login/', {
            'email': 'test@test.com',
            'password': 'password123',
        })
        self.assertRedirects(response, '/dashboard/')

    def test_login_wrong_password(self):
        response = self.client.post('/login/', {
            'email': 'test@test.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.post('/login/', {
            'email': 'test@test.com',
            'password': 'password123',
        })
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/login/')
