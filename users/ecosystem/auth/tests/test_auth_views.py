from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.middleware.csrf import get_token
from users.models import User, UserLogin, UserGender
from datetime import datetime

is_CSRF = True

class TestAuthLogInViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

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

# class TestAuthLogOutViewSet(TestCase):
    
#     def setUp(self):
#         self.client = Client(enforce_csrf_checks=is_CSRF)
#         self.list_url = reverse('account-log-out-list')
#         date_time_str = '12/31/1990'
#         self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
#         self.client.get(reverse('x-fct-list'))
#         self.csrftoken = self.client.cookies['csrftoken'].value

#         self.user = User.objects.create(
#             first_name = "Desmond",
#             last_name = 'Fox',
#             email = 'fox@foxbecoding.com',
#             password = make_password('123456'),
#             date_of_birth = self.date_time_obj.date(),
#             agreed_to_toa = True
#         )
#         self.user.save()

#     def test_account_log_out_create(self):
#         #set request data
#         request_data = {
#             'email': 'fox@foxbecoding.com',
#             'password': '123456'
#         }
    
#         #Log in user
#         self.client.post(reverse('account-log-in-list'), request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
        
#         #Get updated token
#         csrftoken = self.client.cookies['csrftoken'].value
        
#         #Get response data
#         res = self.client.post(self.list_url, {}, **{'HTTP_X_CSRFTOKEN': csrftoken})

#         #check if data is correct
#         self.assertEqual(res.status_code, 200)