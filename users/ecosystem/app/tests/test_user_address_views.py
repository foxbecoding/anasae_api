from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime

is_CSRF = True

class TestUserAddressViewSet(TestCase):
 
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        user_data = {
            'first_name': "Anasae",
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

        user_address_data = { 
            'full_name': 'Desmond Fox',
            'phone_number': '(504)366-7899',
            'street_address': '1912 Pailet',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Harvey',
            'postal_code': '70058'
        }
        user_address_res = self.client.post(
            reverse('user-address-list'), 
            data=user_address_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.user_address_pk = user_address_res.data['addresses'][0]['pk']
        

    def test_user_address_create(self):
        request_data = { 
            'full_name': 'Desmond Fox',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmoor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072'
        }
        res = self.client.post(
            reverse('user-address-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 

        self.assertEqual(res.data['addresses'][1]['city'], 'Marrero')
        self.assertEqual(res.status_code, 201)
    
    def test_user_address_create_error(self):
        request_data = { 
            'full_name': '',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072'
        }
        res = self.client.post(
            reverse('user-address-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 400)

    def test_user_address_update(self):
        request_data = { 
            'full_name': 'Desmond L Fox',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072',
            'is_default': True
        }
        
        res = self.client.put(
            reverse('user-address-detail', kwargs={'pk': self.user_address_pk}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 202)

    def test_user_address_update_error(self):
        request_data = { 
            'full_name': '',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072',
            'is_default': True
        }
        res = self.client.put(
            reverse('user-address-detail', kwargs={'pk': self.user_address_pk}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 400)

    def test_user_address_update_permissions_failed(self):
        request_data = { 
            'full_name': 'Desmond L Fox',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmor dr',
            'street_address_ext': '',
            'country': 'United States',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072',
            'is_default': True
        }
        res = self.client.put(
            reverse('user-address-detail', kwargs={'pk': 847}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 403)
    
    def test_user_address_destroy(self):
        request_data = {}
        res = self.client.delete(
            reverse('user-address-detail', kwargs={'pk': self.user_address_pk}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 202)
    
    def test_user_address_destroy_permissions_failed(self):
        request_data = {}
        res = self.client.delete(
            reverse('user-address-detail', kwargs={'pk': 847}),
            content_type='application/json',
            data=request_data,  
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.assertEqual(res.status_code, 403)