from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime

is_CSRF = True

class TestBrandFollowerViewSet(TestCase):
 
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_str = '12/31/1990'
        self.date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        user_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_obj.date(),
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

        brand_request_data = { 
            'name': 'Fenty Beauty',
            'bio': 'Fenty Beauty by Rihanna was created with promise of inclusion for all women. With an unmatched offering of shades and colors for ALL skin tones, you&#39;ll never look elsewhere for your beauty staples. Browse our foundation line, lip colors, and so much more.'
        }

        brand_res = self.client.post(
            reverse('brand-list'), 
            data=brand_request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.brand_data = brand_res.data

    def test_brand_follower_create(self):   
        request_data = {
            'brand': self.brand_data['pk']
        }

        res = self.client.post(
            reverse('brand-follower-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        self.assertGreater(res.data['followers'], 0)
        self.assertEqual(res.status_code, 201)   
    
    def test_brand_follower_create_permissions_failed(self):   
        request_data = {
            'brand': ''
        }

        res = self.client.post(
            reverse('brand-follower-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 403)   
    
    def test_brand_follower_create_errors(self):
        request_data = {
            'brand': self.brand_data['pk']
        }

        self.client.post(
            reverse('brand-follower-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        res = self.client.post(
            reverse('brand-follower-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        print(res.data)

        self.assertEqual(res.status_code, 400)   