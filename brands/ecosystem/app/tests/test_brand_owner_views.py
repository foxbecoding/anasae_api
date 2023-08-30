from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from utils.helpers import list_to_str

is_CSRF = True

class TestBrandOwnerViewSet(TestCase):
 
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        self.date_time_str = '12/31/1990'

        user_data = {
            'first_name': "Desmond",
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

        login_credentials = {
            'username': 'slugga',
            'password': '123456'
        }
    
        login_res = self.client.post(
            reverse('auth-log-in-list'), 
            login_credentials, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.user = login_res.data
        self.csrftoken = self.client.cookies['csrftoken'].value

        brand_request_data = { 
            'name': 'Fenty Beauty',
            'bio': 'Fenty Beauty by Rihanna was created with promise of inclusion for all women. With an unmatched offering of shades and colors for ALL skin tones, you&#39;ll never look elsewhere for your beauty staples. Browse our foundation line, lip colors, and so much more.'
        }

        brand_res = self.client.post(
            reverse('brand-list'), 
            data=brand_request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.brand_data = brand_res.data

    def test_brand_owner_create(self):
        user_data = {
            'first_name': "Rihhana",
            'last_name': 'Fenty',
            'email': 'riri@fentybeauty.com',
            'username': 'badgalriri',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_str,
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        user_res = self.client.post(
            reverse('user-list'), 
            user_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        request_data = {
            'brand': self.brand_data['pk'],
            'user': user_res.data['pk']
        }

        res = self.client.post(
            reverse('brand-owner-list'), 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        self.assertGreater(len(res.data['owners']), 1)
        self.assertEqual(res.status_code, 201)   
    
    def test_brand_owner_create_errors(self):
        user_data = {
            'first_name': "Rihhana",
            'last_name': 'Fenty',
            'email': 'riri@fentybeauty.com',
            'username': 'badgalriri',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_str,
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        user_res = self.client.post(
            reverse('user-list'), 
            user_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        request_data = {
            'brand': self.brand_data['pk'],
            'user': ''
        }

        res = self.client.post(
            reverse('brand-owner-list'), 
            data=request_data,
            content_type='application/json', 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 400)   
    
    def test_brand_owner_create_owner_errors(self):
        request_data = {
            'brand': self.brand_data['pk'],
            'user': self.user['pk']
        }

        res = self.client.post(
            reverse('brand-owner-list'), 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 400)   

    def test_brand_owner_retrieve(self):
        owners = [ owner['pk'] for owner in self.brand_data['owners'] ]
        res = self.client.get(reverse('brand-owner-detail', kwargs={'pk': list_to_str(owners)}))
        self.assertGreater(len(res.data), 0)
        self.assertEqual(res.status_code, 200)