from django.test import TestCase, Client
from django.urls import reverse
from django.middleware.csrf import get_token
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

    def test_user_create(self):
        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        request_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'fox@foxbecoding.com',
            'username': 'foxbecoding.com',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        print(request_data)
        # res = self.client.post(
        #     reverse('user-list'), 
        #     request_data, 
        #     **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        # )
  
        #check if data is correct
        # self.assertEqual(res.data['gender_choice'], 1)
        # self.assertGreater(len(res.data['profiles']), 0)
        # self.assertEqual(res.data['first_name'], 'Desmond')
        # self.assertEqual(res.status_code, 201)
    
    # def test_account_sign_up_create_no_data(self):
    #     #set request data
    #     request_data = {}

    #     #Get response data
    #     res = self.client.post(self.list_url, request_data, **{'HTTP_X_CSRFTOKEN': self.csrftoken})

    #     #check if data is correct
    #     self.assertEqual(res.status_code, 400)