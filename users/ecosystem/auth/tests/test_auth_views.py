from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.middleware.csrf import get_token
from users.models import User, UserLogin, UserGender
from datetime import datetime

is_CSRF = True

# class TestAccountSignUpViewSet(TestCase):
    
#     def setUp(self):
#         self.client = Client(enforce_csrf_checks=is_CSRF)
#         self.list_url = reverse('account-sign-up-list')
#         self.client.get(reverse('x-fct-list'))
#         self.csrftoken = self.client.cookies['csrftoken'].value

#         self.user_gender = UserGender.objects.create(gender = 'male')
#         self.user_gender.save()

#     def test_account_sign_up_create(self):
#         #set request data
#         date_time_str = '12/31/1990'
#         date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

#         request_data = {
#             'first_name': "Desmond",
#             'last_name': 'Fox',
#             'email': 'fox@foxbecoding.com',
#             'password': '123456',
#             'confirm_password': '123456',
#             'date_of_birth': date_time_obj.date(),
#             'agreed_to_toa': True,
#             'gender': self.user_gender.pk
#         }

#         #Get response data
#         res = self.client.post(self.list_url, request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
  
#         #check if data is correct
#         self.assertEqual(res.data['gender_choice'], 1)
#         self.assertGreater(len(res.data['profiles']), 0)
#         self.assertEqual(res.data['first_name'], 'Desmond')
#         self.assertEqual(res.status_code, 201)
    
#     def test_account_sign_up_create_no_data(self):
#         #set request data
#         request_data = {}

#         #Get response data
#         res = self.client.post(self.list_url, request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})

#         #check if data is correct
#         self.assertEqual(res.status_code, 400)


class TestAuthLogInViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.list_url = reverse('account-log-in-list')
        date_time_str = '12/31/1990'
        self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value

        self.user = User.objects.create(
            first_name = "Desmond",
            last_name = 'Fox',
            email = 'fox@foxbecoding.com',
            password = make_password('123456'),
            date_of_birth = self.date_time_obj.date(),
            agreed_to_toa = True
        )
        self.user.save()

    def test_account_log_in_create(self):
        #set request data
        request_data = {
            'email': 'fox@foxbecoding.com',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(self.list_url, request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})

        #check if data is correct
        self.assertGreater(len(res.data['logins']), 0)
        self.assertEqual(res.data['first_name'], 'Desmond')
        self.assertEqual(res.status_code, 202)

    def test_account_log_in_create_failed(self):
        #set request data
        request_data = {
            'email': 'fox@foxbecoding.com',
        }
    
        #Get response data
        res = self.client.post(self.list_url, request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})

        #check if data is correct
        self.assertEqual(res.status_code, 400)

class TestAuthLogOutViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.list_url = reverse('account-log-out-list')
        date_time_str = '12/31/1990'
        self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value

        self.user = User.objects.create(
            first_name = "Desmond",
            last_name = 'Fox',
            email = 'fox@foxbecoding.com',
            password = make_password('123456'),
            date_of_birth = self.date_time_obj.date(),
            agreed_to_toa = True
        )
        self.user.save()

    def test_account_log_out_create(self):
        #set request data
        request_data = {
            'email': 'fox@foxbecoding.com',
            'password': '123456'
        }
    
        #Log in user
        self.client.post(reverse('account-log-in-list'), request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})
        
        #Get updated token
        csrftoken = self.client.cookies['csrftoken'].value
        
        #Get response data
        res = self.client.post(self.list_url, {}, **{'HTTP_X_CSRFTOKEN': csrftoken})

        #check if data is correct
        self.assertEqual(res.status_code, 200)