from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from categories.ecosystem.methods import test_categories
from pprint import pprint

is_CSRF = True

class TestCartViewSet(TestCase):
 
    def setUp(self):
        self.categories = test_categories()
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
            'name': 'ANASAE',
            'bio': 'ANASAE has all of the essentials for all of your needs.  Shop with us today!',
        }

        brand_res = self.client.post(
            reverse('brand-list'), 
            data=brand_request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.brand_data = brand_res.data

        product_request_data = {
            'brand': self.brand_data['pk'],
            'category': self.categories['category_data']['pk'],
            'subcategory': self.categories['subcategory_data']['pk'],
            'title': "Black chinos dress pants for men",
            'description': 'Black chinos dress pants for men',
            'quantity': 20,
            'sku': None,
            'is_active': True,
            'variant_order': 1
        }
        
        product_res = self.client.post(
            reverse('product-list'), 
            data=[product_request_data], 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.product_data = product_res.data

        cart_res = self.client.get(reverse('cart-list'))
        request_data = {
            'cart': cart_res.data['pk'],
            'item': self.product_data[0]['pk'],
            'quantity': 1
        }

        res = self.client.post(
            reverse('cart-item-list'),
            request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        

    def test_cart_list(self):
        res = self.client.get(reverse('cart-list'))
        self.assertEqual(res.status_code, 200)

    # def test_cart_item_create(self):
    #     cart_res = self.client.get(reverse('cart-list'))
    #     request_data = {
    #         'cart': cart_res.data['pk'],
    #         'item': self.product_data[0]['pk'],
    #         'quantity': 3
    #     }

    #     res = self.client.post(
    #         reverse('cart-item-list'),
    #         request_data, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )

    #     cart_res = self.client.get(reverse('cart-list'))
    #     self.assertGreater(len(cart_res.data['items']), 0)
    #     self.assertEqual(res.status_code, 201)

    # def test_cart_update(self):
    #     cart_res = self.client.get(reverse('cart-list'))
    #     cart_item_pk = cart_res.data['items'][0]['pk']
    #     res = self.client.put(
    #         reverse('cart-item-detail', kwargs={'pk': cart_item_pk}),
    #         {'quantity': 9}, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )
    #     self.assertGreater(res.data['items'][0]['quantity'], cart_res.data['items'][0]['quantity'])
    #     self.assertEqual(res.status_code, 202)
    
    # def test_cart_delete(self):
    #     cart_res = self.client.get(reverse('cart-list'))
    #     cart_item_pk = cart_res.data['items'][0]['pk']
    #     res = self.client.delete(
    #         reverse('cart-item-detail', kwargs={'pk': cart_item_pk}),
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )

    #     self.assertEqual(len(res.data['items']), 0)
    #     self.assertEqual(res.status_code, 202)