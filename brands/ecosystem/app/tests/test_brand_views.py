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

    def test_brand_create(self):
        request_data = { 
            'name': 'ANASAE',
            'bio': 'ANASAE has all of the essentials for all of your needs.  Shop with us today!',
        }
        res = self.client.post(
            reverse('brand-list'), 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 

        self.assertEqual(res.data['name'], 'ANASAE')
        self.assertGreater(len(res.data['owners']), 0)
        self.assertEqual(res.status_code, 201)
    
    def test_brand_create_error(self):
        request_data = { 
            'name': '',
            'bio': 'ANASAE has all of the essentials for all of your needs.  Shop with us today!',
        }
        res = self.client.post(
            reverse('brand-list'), 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 400)

    def test_brand_retrieve(self):
        res = self.client.get(
            reverse('brand-detail', kwargs={'pk': self.brand_data['pk']}),
        )

        self.assertEqual(res.status_code, 200)
    
    def test_brand_update(self):
        request_data = { 
            'name': 'Fenty x Savage',
            'bio': 'Fenty Beauty by Rihanna was created with promise of inclusion for all women. With an unmatched offering of shades and colors for ALL skin tones, you&#39;ll never look elsewhere for your beauty staples. Browse our foundation line, lip colors, and so much more.'
        }
        res = self.client.put(
            reverse('brand-detail', kwargs={'pk': self.brand_data['pk']}),
            data=request_data,
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.data['name'], 'Fenty x Savage')
        self.assertEqual(res.status_code, 202)
    
    def test_brand_update_error(self):
        request_data = { 
            'name': '',
            'bio': 'Fenty Beauty by Rihanna was created with promise of inclusion for all women. With an unmatched offering of shades and colors for ALL skin tones, you&#39;ll never look elsewhere for your beauty staples. Browse our foundation line, lip colors, and so much more.'
        }
        res = self.client.put(
            reverse('brand-detail', kwargs={'pk': self.brand_data['pk']}),
            data=request_data,
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 400)

    def test_brand_permissions_failed(self):
        request_data = { 
            'name': 'Fenty x Savage',
            'bio': 'Fenty Beauty by Rihanna was created with promise of inclusion for all women. With an unmatched offering of shades and colors for ALL skin tones, you&#39;ll never look elsewhere for your beauty staples. Browse our foundation line, lip colors, and so much more.'
        }
        res = self.client.put(
            reverse('brand-detail', kwargs={'pk': 154}),
            data=request_data,
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(res.status_code, 403)