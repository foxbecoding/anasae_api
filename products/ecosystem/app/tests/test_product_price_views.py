from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from categories.ecosystem.methods import test_categories
from datetime import datetime

is_CSRF = True

class TestProductPriceViewSet(TestCase):
 
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

    def test_product_price_create(self):
        request_data = []
        for product in self.products:
            request_data.append({
                'price': 2999,
                'product': product['pk']
            })
        
        price_res = self.client.post(
            reverse('product-price-list'), 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 

        product_pks = [ str(data['product']) for data in price_res.data ]
        product_pks = ','.join(product_pks)
        products_res = self.client.get(
            reverse('product-list')+f'?pks={product_pks}', 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        print(products_res.data)
        # self.assertEqual(price_res.data[0]['price'], 2999)
        # self.assertEqual(price_res.status_code, 201)
    
    # def test_product_price_create_errors(self):
    #     request_data = []
    #     for product in self.products:
    #         request_data.append({
    #             'price': '',
    #             'product': product['pk']
    #         })
        
    #     res = self.client.post(
    #         reverse('product-price-list'), 
    #         data=request_data, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 

    #     self.assertEqual(res.status_code, 400)
    
    # def test_product_price_create_permissions_failed(self):
    #     request_data = []
    #     for product in self.products:
    #         request_data.append({
    #             'price': 2999,
    #             'product': 158
    #         })
        
    #     res = self.client.post(
    #         reverse('product-price-list'), 
    #         data=request_data, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 

    #     self.assertEqual(res.status_code, 403)

    # def test_product_price_update(self):
    #     request_data = []
    #     for product in self.products:
    #         request_data.append({
    #             'price': 2999,
    #             'product': product['pk']
    #         })
        
    #     price_data = self.client.post(
    #         reverse('product-price-list'), 
    #         data=request_data, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ).data
    #     price_data = price_data[0]
    #     price_pk = price_data['pk']
    #     product_pk = price_data['product']

    #     res = self.client.put(
    #         reverse('product-price-detail', kwargs={'pk': price_pk}), 
    #         data={'price': 3999, 'product': product_pk}, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 

    #     self.assertEqual(res.data['price'], 3999)
    #     self.assertEqual(res.status_code, 202)
    
    # def test_product_price_update_errors(self):
    #     request_data = []
    #     for product in self.products:
    #         request_data.append({
    #             'price': 2999,
    #             'product': product['pk']
    #         })
        
    #     price_data = self.client.post(
    #         reverse('product-price-list'), 
    #         data=request_data, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ).data
    #     price_data = price_data[0]
    #     price_pk = price_data['pk']
    #     product_pk = price_data['product']

    #     res = self.client.put(
    #         reverse('product-price-detail', kwargs={'pk': price_pk}), 
    #         data={'price': '', 'product': product_pk}, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 

    #     self.assertEqual(res.status_code, 400)
    
    # def test_product_price_update_permissions_failed(self):
    #     request_data = []
    #     for product in self.products:
    #         request_data.append({
    #             'price': 2999,
    #             'product': product['pk']
    #         })
        
    #     price_data = self.client.post(
    #         reverse('product-price-list'), 
    #         data=request_data, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ).data
    #     price_data = price_data[0]
    #     price_pk = price_data['pk']
    #     product_pk = price_data['product']

    #     res = self.client.put(
    #         reverse('product-price-detail', kwargs={'pk': price_pk}), 
    #         data={'price': 3999}, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     ) 

    #     self.assertEqual(res.status_code, 403)