from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from categories.ecosystem.methods import test_categories
from products.models import ProductListing
from datetime import datetime
from pprint import pprint

is_CSRF = True

class TestProductViewSet(TestCase):
 
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
            'is_active': True
        }
        
        product_res = self.client.post(
            reverse('product-list'), 
            data=[product_request_data], 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.product_data = product_res.data

    # def test_product_create(self):
    #     request_data = []
    #     product_data = [
    #         {
    #             'title': "Business casual navy blue chinos for men 34",
    #             'description': 'Business casual navy blue chinos for men'
    #         },
    #         {
    #             'title': "Business casual navy blue chinos for men 36",
    #             'description': 'Business casual navy blue chinos for men '
    #         }
    #     ]
    #     for data in product_data:
    #         product = {
    #             'brand': self.brand_data['pk'],
    #             'category': self.categories['category_data']['pk'],
    #             'subcategory': self.categories['subcategory_data']['pk'],
    #             'title': data['title'],
    #             'description': data['description'],
    #             'quantity': 20,
    #             'sku': None,
    #             'is_active': True
    #         }

    #         request_data.append(product)

    #     res = self.client.post(
    #         reverse('product-list'), 
    #         data=request_data, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 

    #     self.assertGreater(len(res.data), 1)
    #     self.assertEqual(res.status_code, 201)
    
    def test_product_create_with_listing_id(self):
        listing_ins = ProductListing.objects.get(pk=self.product_data[0]['listing'])
        request_data = []
        product_data = [
            {
                'title': "Business casual navy blue chinos for men 34",
                'description': 'Business casual navy blue chinos for men'
            },
            {
                'title': "Business casual navy blue chinos for men 36",
                'description': 'Business casual navy blue chinos for men '
            }
        ]
        for data in product_data:
            product = {
                'brand': self.brand_data['pk'],
                'category': self.categories['category_data']['pk'],
                'subcategory': self.categories['subcategory_data']['pk'],
                'title': data['title'],
                'description': data['description'],
                'quantity': 20,
                'sku': None,
                'is_active': True
            }

            request_data.append(product)

        res = self.client.post(
            reverse('product-list')+f'?lid={listing_ins.uid}', 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 

        self.assertGreater(len(res.data), 1)
        self.assertEqual(res.status_code, 201)

    # def test_product_create_permissions_failed(self):
    #     request_data = {
    #         'brand': 155,
    #         'category': self.categories['category_data']['pk'],
    #         'subcategory': self.categories['subcategory_data']['pk'],
    #         'title': "Business casual navy blue chinos for men",
    #         'description': 'Business casual navy blue chinos for men',
    #         'quantity': 20,
    #         'sku': None,
    #         'is_active': True
    #     }
        
    #     res = self.client.post(
    #         reverse('product-list'), 
    #         data=[request_data],
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 

    #     self.assertEqual(res.status_code, 403)

    # def test_product_create_errors(self):
    #     request_data = {
    #         'brand': self.brand_data['pk'],
    #         'category': self.categories['category_data']['pk'],
    #         'subcategory': self.categories['subcategory_data']['pk'],
    #         'title': "",
    #         'description': 'Business casual navy blue chinos for men',
    #         'quantity': 20,
    #         'sku': None,
    #         'is_active': True
    #     }
        
    #     res = self.client.post(
    #         reverse('product-list'), 
    #         data=[request_data],
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 
        
    #     self.assertEqual(res.status_code, 400)

    # def test_product_retrieve(self):
    #     res = self.client.get(
    #         reverse('product-detail', kwargs={'pk': self.product_data[0]['pk']})
    #     ) 
    #     self.assertEqual(res.data['title'], 'Black chinos dress pants for men')
    #     self.assertEqual(res.status_code, 200)
    
    # def test_product_update(self):
    #     request_data = {
    #         'title': "Black chinos dress pants for men",
    #         'description': 'Black chinos dress pants for men',
    #         'quantity': 25,
    #         'sku': None,
    #         'is_active': True
    #     }
    #     res = self.client.put(
    #         reverse('product-detail', kwargs={'pk': self.product_data[0]['pk']}),
    #         request_data,
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 
        
    #     self.assertEqual(res.data['quantity'], 25)
    #     self.assertEqual(res.status_code, 202)
    
    # def test_product_update_errors(self):
    #     request_data = {
    #         'title': "",
    #         'description': 'Black chinos dress pants for men',
    #         'quantity': 25,
    #         'sku': None,
    #         'is_active': True
    #     }
    #     res = self.client.put(
    #         reverse('product-detail', kwargs={'pk': self.product_data[0]['pk']}),
    #         request_data,
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 
        
    #     self.assertEqual(res.status_code, 400)