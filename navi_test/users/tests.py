from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.


User = get_user_model()


class CreateUserTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "som", "email": "som@gmail.com", "password": "password"}

    def test_user_can_signup(self):
        response = self.client.post(reverse('signup'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validate_email(self):
        self.user_data['email'] = "som@sdasdadas.com"
        response = self.client.post(reverse('signup'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTest(APITestCase):

    def setUp(self):
        self.user_data = {"username": "som", "email": "som@gmail.com", "password": "password"}
        self.user = User.objects.create_user(**self.user_data)


    def test_user_can_login(self):
        user_data = {"username": "som", "password": "password"}
        response = self.client.post(reverse('login'), user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_can_receive_token(self):
        user_data = {"username": "som", "password": "password"}
        response = self.client.post(reverse('login'), user_data)
        self.assertIn('token', response.data)


class AuthenticateRequestWithJWTToken(APITestCase):

    def setUp(self):
        self.user_data = {"username": "som", "email": "som@gmail.com", "password": "password"}
        self.user = User.objects.create_user(**self.user_data)
        self.token = self.client.post(reverse('login'), self.user_data).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def test_can_authenticate_with_jwt(self):
        response = self.client.get(reverse('hello'))
        self.assertIn('hello', response.data['message'])

