from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

class RegisterTestCase(APITestCase):
    def  test_register(self):
        data = { 
            "username": "test",
            "email": "testcase@example.com",
            "password": "testpwd",
            "password2": "testpwd",
        }

        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogOutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test@example.com')
        self.client.force_authenticate(self.user)
        
    def test_login(self):
        data = {
            "username": "test",
            "password": "test@example.com",
        }
        
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    