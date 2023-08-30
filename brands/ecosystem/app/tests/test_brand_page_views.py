from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime
from pprint import pprint

is_CSRF = True

class TestBrandPageViewSet(TestCase):
 
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_str = '12/31/1990'
        
        user_data = {
            'first_name': "Desmond",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_str,
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

    def test_brand_page_retrieve_logged_in(self):
        brand_res = self.client.get(
            reverse('brand-page-detail', kwargs={ 'uid': self.brand_data['uid'] }),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertTrue(brand_res.data['isOwner'])
        self.assertEquals(brand_res.status_code, 200)
    
    def test_brand_page_retrieve_not_logged_in(self):
        self.client.post(
            reverse('auth-log-out-list'), 
            {}, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        brand_res = self.client.get(
            reverse('brand-page-detail', kwargs={ 'uid': self.brand_data['uid'] }),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertFalse(brand_res.data['isOwner'])
        self.assertEquals(brand_res.status_code, 200)
    
    def test_brand_page_retrieve_not_found(self):
        brand_res = self.client.get(
            reverse('brand-page-detail', kwargs={ 'uid': 'fdfsds' }),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEquals(brand_res.status_code, 404)