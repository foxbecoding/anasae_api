from django.test import TestCase, Client
from django.urls import reverse
from django.middleware.csrf import get_token
from users.models import User, UserGender
from datetime import datetime

is_CSRF = True

class TestUserViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        user_data = {
            'first_name': "Lavell",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        self.client.post(
            reverse('user-list'), 
            user_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        #User Login
        login_credentials = {
            'email': 'slugga@gmail.com',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(
            reverse('auth-log-in-list'), 
            login_credentials, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.user = res.data
        self.csrftoken = self.client.cookies['csrftoken'].value

    def test_user_create(self):
        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'username': 'foxbecoding',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        res = self.client.post(
            reverse('user-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.data['first_name'], 'Desmond')
        self.assertEqual(res.status_code, 201)
    
    def test_user_create_permissions_failed(self):
        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'username': 'foxbecoding',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True
        }

        res = self.client.post(
            reverse('user-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 403)
    
    def test_user_create_errors(self):
        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'username': 'foxbecoding',
            'password': '123456',
            'confirm_password': '1234567',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        res = self.client.post(
            reverse('user-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        self.assertEqual(res.status_code, 400)

    def test_user_retrieve(self):
        pass