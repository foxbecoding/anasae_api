from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime
import stripe
from pprint import pprint

is_CSRF = True

class TestUserBillingAddressViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        self.date_time_str = '12/31/1990'

        user_data = {
            'first_name': "Lavell",
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

        #User Login
        login_credentials = {
            'username': 'slugga',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(
            reverse('auth-log-in-list'), 
            login_credentials, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.user = res.data
        self.csrftoken = self.client.cookies['csrftoken'].value
        
        setup_intent_create_res = stripe.SetupIntent.create(
            customer=self.user['stripe_customer_id'],
            payment_method="pm_card_visa"
        )
        
        self.setup_intent_confirm_res = stripe.SetupIntent.confirm(
            setup_intent_create_res.id,
            payment_method="pm_card_visa"
        )

        payment_method_res = self.client.post(
            reverse('user-payment-method-list'),
            data = {'payment_method_id': self.setup_intent_confirm_res.payment_method},
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        user_address_data = { 
            'full_name': 'Desmond Fox',
            'phone_number': '(504)366-7899',
            'street_address': '1912 Pailet',
            'street_address_ext': '',
            'country': 'US',
            'state': 'Louisiana',
            'city': 'Harvey',
            'postal_code': '70058'
        }
        user_address_res = self.client.post(
            reverse('user-address-list'), 
            data=user_address_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        user_address_data2 = { 
            'full_name': 'Desmond Fox',
            'phone_number': '(504)729-8617',
            'street_address': '4024 Crossmoor Dr',
            'street_address_ext': '',
            'country': 'US',
            'state': 'Louisiana',
            'city': 'Marrero',
            'postal_code': '70072'
        }
        user_address_res2 = self.client.post(
            reverse('user-address-list'), 
            data=user_address_data2, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.user_address_pk = user_address_res.data['addresses'][0]['pk']
        self.user_address2_pk = user_address_res2.data['addresses'][1]['pk']
        self.payment_method_pk = payment_method_res.data['payment_methods'][0]['pk']

    def test_user_billing_address_create(self):
        request_data = {
            'address': self.user_address_pk,
            'payment_method': self.payment_method_pk
        }

        res = self.client.post(
            reverse('user-billing-address-list'),
            data = request_data,
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertGreater(len(res.data['billing_addresses']), 0)
        self.assertEqual(res.status_code, 201)
    
    def test_user_billing_address_update(self):
        request_data = {
            'address': self.user_address_pk,
            'payment_method': self.payment_method_pk
        }

        res = self.client.post(
            reverse('user-billing-address-list'),
            data = request_data,
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        billing_address_pk = res.data['billing_addresses'][0]['pk']
  
        edit_res = self.client.put(
            reverse('user-billing-address-detail', kwargs={'pk': billing_address_pk}),
            data = {
                'address': self.user_address2_pk,
                'payment_method': self.payment_method_pk,
            },
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        self.assertNotEqual(edit_res.data['billing_addresses'][0]['address'], self.user_address_pk)
        self.assertEqual(edit_res.status_code, 202)