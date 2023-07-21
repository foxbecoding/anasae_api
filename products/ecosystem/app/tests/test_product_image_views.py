from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from categories.ecosystem.methods import test_categories
from datetime import datetime
from utils.helpers import list_to_str, key_exists, tmp_image
from pprint import pprint
import json
from PIL import Image

is_CSRF = True

class TestProductImageViewSet(TestCase):
 
    def setUp(self):
        self.categories = test_categories()
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        User_Gender_Instance.save()

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
            'gender': User_Gender_Instance.id
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
        user = login_res.data
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
        brand_data = brand_res.data
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
                'brand': brand_data['pk'],
                'category': self.categories['category_data']['pk'],
                'subcategory': self.categories['subcategory_data']['pk'],
                'title': data['title'],
                'description': data['description'],
                'quantity': 20,
                'sku': None,
                'isbn': None
            }

            request_data.append(product)
    
        res = self.client.post(
            reverse('product-list'), 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.products = res.data

    def test_product_image_create(self):
        request_data = []
        images = [ tmp_image('png') for i in range(7) ]
        for product in self.products:
            request_data.append({'images': images, 'product': product['pk']})

        for data in request_data[0:1]:
            res = self.client.post(
                reverse('product-image-list'), 
                data=data,
                **{'HTTP_X_CSRFTOKEN': self.csrftoken}
            )
            product_pk = res.data[0]['product']
            product_res = self.client.get(
                reverse('product-detail', kwargs={"pk": product_pk}), 
                content_type='application/json',
                **{'HTTP_X_CSRFTOKEN': self.csrftoken}
            )
            print(product_res.data)
            self.assertEqual(res.status_code, 201)

    # def test_product_image_create_errors(self):
    #     request_data = []
    #     images = [ tmp_image('gif') for i in range(7) ]
    #     for product in self.products:
    #         request_data.append({'images': images, 'product': product['pk']})

    #     for data in request_data[0:1]:
    #         res = self.client.post(
    #             reverse('product-image-list'), 
    #             data=data,
    #             **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #         )
            
    #         self.assertEqual(res.status_code, 400)
    
    # def test_product_image_create_permissions_failed(self):
    #     request_data = []
    #     images = [ tmp_image('png') for i in range(7) ]
    #     for product in self.products:
    #         request_data.append({'images': images, 'product': 111})

    #     for data in request_data[0:1]:
    #         res = self.client.post(
    #             reverse('product-image-list'), 
    #             data=data,
    #             **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #         )
            
    #         self.assertEqual(res.status_code, 403)

    # def test_product_image_delete(self):
    #     request_data = []
    #     images = [ tmp_image('png') for i in range(7) ]
    #     for product in self.products:
    #         request_data.append({'images': images, 'product': product['pk']})

    #     for data in request_data[0:1]:
    #         create_res = self.client.post(
    #             reverse('product-image-list'), 
    #             data=data,
    #             **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #         )
            
    #         image_pks = list_to_str(list(dict.fromkeys([ data['pk'] for data in create_res.data[0:3] ])))
            
    #         delete_res = self.client.delete(
    #             reverse('product-image-detail', kwargs={"pk": image_pks}), 
    #             data=data,
    #             **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #         )

    #         self.assertEqual(delete_res.status_code, 202)