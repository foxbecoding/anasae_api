from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime

is_CSRF = True

class TestBrandViewSet(TestCase):
 
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

        login_credentials = {
            'username': 'slugga',
            'password': '123456'
        }
    
        login_res = self.client.post(
            reverse('auth-log-in-list'), 
            login_credentials, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.user = login_res.data
        self.csrftoken = self.client.cookies['csrftoken'].value

    def test_brand_create(self):
        request_data = { 
            'name': 'ANASAE',
            'bio': 'ANASAE has all of the essentials for all of your needs.  Shop with us today!',
        }
        res = self.client.post(
            reverse('brand-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        print(res.data)
        # self.assertEqual(res.data['addresses'][1]['city'], 'Marrero')
        # self.assertEqual(res.status_code, 201)
    
    # def test_brand_create_error(self):
    #     request_data = { 
    #         'full_name': '',
    #         'phone_number': '(504)729-8617',
    #         'street_address': '4024 Crossmor dr',
    #         'street_address_ext': '',
    #         'country': 'United States',
    #         'state': 'Louisiana',
    #         'city': 'Marrero',
    #         'postal_code': '70072'
    #     }
    #     res = self.client.post(
    #         reverse('user-address-list'), 
    #         data=request_data, 
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )
    #     self.assertEqual(res.status_code, 400)