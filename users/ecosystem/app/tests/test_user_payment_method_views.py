from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime
import stripe
from pprint import pprint

is_CSRF = True

class TestUserPaymentMethodViewSet(TestCase):
    
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

        self.payment_method = self.client.post(
            reverse('user-payment-method-list'),
            data = {'payment_method_id': self.setup_intent_confirm_res.payment_method},
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ).data['payment_methods']

    def test_user_payment_method_get_client_secret_list(self):
        res = self.client.get(reverse('user-payment-method-list'))
        self.assertEqual(res.status_code, 200)

    def test_user_payment_method_create(self):
        res = self.client.post(
            reverse('user-payment-method-list'),
            data = {'payment_method_id': self.setup_intent_confirm_res.payment_method},
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertGreater(len(res.data['payment_methods']), 0)
        self.assertEqual(res.status_code, 201)

    def test_user_payment_method_retrieve(self):
        payment_method = self.payment_method[0]
        res = self.client.get(
            reverse('user-payment-method-detail', kwargs={'pk': payment_method['pk']}),
            content_type='application/json'
        )

        self.assertEqual(res.data[0].id, payment_method['stripe_pm_id'])
        self.assertEqual(res.status_code, 200)

    def test_user_payment_method_destroy(self):
        payment_method = self.payment_method[0]
        delete_res = self.client.delete(
            reverse(
                'user-payment-method-detail',
                kwargs={'pk': payment_method['pk']}
            ),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(len(delete_res.data['payment_methods']), 0)
        self.assertEqual(delete_res.status_code, 202)

    def test_user_payment_method_destroy_permissions_failed(self):
        self.client.post(
            reverse('user-payment-method-list'),
            data = {'payment_method_id': self.setup_intent_confirm_res.payment_method},
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        delete_res = self.client.delete(
            reverse(
                'user-payment-method-detail',
                kwargs={'pk': 504}
            ),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEqual(delete_res.status_code, 403)