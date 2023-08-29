from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime

is_CSRF = True

class TestUserViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        self.date_time_str = '12/31/1990'

        user_data = {
            'first_name': "Lavell",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_str,
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        self.client.post(
            reverse('user-list'), 
            user_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        #User Login
        login_credentials = {
            'username': 'slugga',
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

        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'username': 'foxbecoding',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_str,
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        res = self.client.post(
            reverse('user-list'), 
            request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.data['first_name'], 'Desmond')
        self.assertEqual(res.status_code, 201)
    
    def test_user_create_permissions_failed(self):

        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'username': 'foxbecoding',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_str,
            'agreed_to_toa': True
        }

        res = self.client.post(
            reverse('user-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 403)
    
    def test_user_create_errors(self):
        
        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'username': 'foxbecoding',
            'password': '123456',
            'confirm_password': '1234567',
            'date_of_birth': self.date_time_str,
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
        res = self.client.get(
            reverse('user-detail', kwargs={'pk': self.user['pk']})
        )

        self.assertEqual(res.data['pk'], self.user['pk'])
        self.assertEqual(res.status_code, 200)

    def test_user_partial_update(self):
        request_data = {
            # 'first_name': "Lavell",
            # 'last_name': 'Fox',
            # 'email': 'slugga@gmail.com',
            # 'username': 'slugga',
            'display_name': 'King Slugga'
        }

        res = self.client.patch(
            reverse('user-detail', kwargs={'pk': self.user['pk']}),
            content_type='application/json',
            data=request_data,
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.data['display_name'], request_data['display_name'])
        self.assertEqual(res.status_code, 202)
    
    def test_user_partial_update_password_change(self):
        request_data = {
            'password': '123456789',
            'confirm_password': '123456789',
        }

        res = self.client.patch(
            reverse('user-detail', kwargs={'pk': self.user['pk']}),
            content_type='application/json',
            data=request_data,
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 202)
    
    def test_user_partial_update_password_change_errors(self):
        request_data = {
            'password': '12345678',
            'confirm_password': '123456789',
        }

        res = self.client.patch(
            reverse('user-detail', kwargs={'pk': self.user['pk']}),
            content_type='application/json',
            data=request_data,
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 400)