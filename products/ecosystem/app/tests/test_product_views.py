from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from categories.ecosystem.methods import test_categories
from pprint import pprint
from datetime import datetime

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

        brand_request_data = { 
            'name': 'ANASAE',
            'bio': 'ANASAE has all of the essentials for all of your needs.  Shop with us today!',
        }

        brand_res = self.client.post(
            reverse('brand-list'), 
            data=brand_request_data, 
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
            'sku': '',
            'isbn': '',
            'price': 2999
        }
        
        product_res = self.client.post(
            reverse('product-list'), 
            data=product_request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        self.product_data = product_res.data

    def test_product_create(self):
        request_data = {
            'brand': self.brand_data['pk'],
            'category': self.categories['category_data']['pk'],
            'subcategory': self.categories['subcategory_data']['pk'],
            'title': "Business casual navy blue chinos for men",
            'description': 'Business casual navy blue chinos for men',
            'quantity': 20,
            'sku': '',
            'isbn': '',
            'price': 2999
        }
        
        res = self.client.post(
            reverse('product-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        
        self.assertEqual(res.data['title'], "Business casual navy blue chinos for men")
        self.assertEqual(res.status_code, 201)
    
    def test_product_create_permissions_failed(self):
        request_data = {
            'brand': 155,
            'category': self.categories['category_data']['pk'],
            'subcategory': self.categories['subcategory_data']['pk'],
            'title': "Business casual navy blue chinos for men",
            'description': 'Business casual navy blue chinos for men',
            'quantity': 20,
            'sku': '',
            'isbn': '',
            'price': 2999
        }
        
        res = self.client.post(
            reverse('product-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 

        self.assertEqual(res.status_code, 403)

    def test_product_create_errors(self):
        request_data = {
            'brand': self.brand_data['pk'],
            'category': self.categories['category_data']['pk'],
            'subcategory': self.categories['subcategory_data']['pk'],
            'title': "",
            'description': 'Business casual navy blue chinos for men',
            'quantity': 20,
            'sku': '',
            'isbn': '',
            'price': 2999
        }
        
        res = self.client.post(
            reverse('product-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 

        self.assertEqual(res.status_code, 400)

    def test_product_retrieve(self):
        res = self.client.get(
            reverse('product-detail', kwargs={'pk': self.product_data['pk']})
        ) 
        print(res.data)
        self.assertEqual(res.data['title'], 'Black chinos dress pants for men')
        self.assertEqual(res.status_code, 200)
    
    def test_product_update(self):
        request_data = {
            'title': "Black chinos dress pants for men",
            'description': 'Black chinos dress pants for men',
            'quantity': 25,
            'sku': '',
            'isbn': ''
        }
        res = self.client.put(
            reverse('product-detail', kwargs={'pk': self.product_data['pk']}),
            request_data,
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 
        
        self.assertEqual(res.data['quantity'], 25)
        self.assertEqual(res.status_code, 202)