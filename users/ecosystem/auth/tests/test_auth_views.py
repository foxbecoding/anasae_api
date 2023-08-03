from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime

is_CSRF = True

class TestAuthLogInViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_obj = datetime.strptime('12/31/1990', '%m/%d/%Y')

        user_data = {
            'first_name': "Desmond",
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

    def test_auth_log_in_create(self):
        request_data = {
            'username': 'slugga',
            'password': '123456'
        }

        res = self.client.post(
            reverse('auth-log-in-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken})

        self.assertGreater(len(res.data['logins']), 0)
        self.assertEqual(res.data['first_name'], 'Desmond')
        self.assertEqual(res.status_code, 202)

    def test_auth_log_in_create_errors(self):
        request_data = {
            'username': 'slugga',
        }
    
        res = self.client.post(
            reverse('auth-log-in-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 400)

class TestAuthLogOutViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_obj = datetime.strptime('12/31/1990', '%m/%d/%Y')

        user_data = {
            'first_name': "Desmond",
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

    def test_auth_log_out_create(self):
        request_data = {
            'username': 'slugga',
            'password': '123456'
        }

        self.client.post(
            reverse('auth-log-in-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        csrftoken = self.client.cookies['csrftoken'].value
        
        res = self.client.post(
            reverse('auth-log-out-list'), 
            {}, 
            **{'HTTP_X_CSRFTOKEN': csrftoken}
        )

        self.assertEqual(res.status_code, 200)

class TestAuthValidateViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_obj = datetime.strptime('12/31/1990', '%m/%d/%Y')

        user_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        self.user_data = self.client.post(
            reverse('user-list'), 
            user_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

    def test_auth_validate_create(self):
        request_data = {
            'username': 'fox',
            'email': 'fox@foxbecoding.com'
        }

        res = self.client.post(
            reverse('auth-validate-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
    
        self.assertEqual(res.status_code, 202)
    
    def test_auth_validate_create_username_exists(self):
        request_data = {
            'username': 'slugga',
            'email': 'fox@foxbecoding.com'
        }

        res = self.client.post(
            reverse('auth-validate-list'), 
            request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
    
        self.assertEqual(res.status_code, 400)