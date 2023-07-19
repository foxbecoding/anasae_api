from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from categories.ecosystem.methods import test_categories
from datetime import datetime
from utils.helpers import list_to_str, key_exists
from pprint import pprint

is_CSRF = True

class TestProductSpecificationViewSet(TestCase):
 
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

    # def test_product_specs_create(self):
    #     spec_values = [
    #         ['Blue', '34', 'Anasae'],
    #         ['Blue', '36', 'Anasae']
    #     ]
    #     product_specs = []
    #     for i, product in enumerate(self.products):
    #         if product['category'] and product['subcategory']:
    #             specifications = self.categories['subcategory_data']['product_specification']
    #             for spec in list(zip(specifications, spec_values[i])):
    #                 data, value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': data['item'],
    #                     'is_required': data['is_required'],
    #                     'value': value.lower(),
    #                     'product': product['pk']
    #                 })
    #         else:
    #             specifications = self.categories['category']['product_specification']
    #             for spec in list(zip(specifications, spec_values[i])):
    #                 data, value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': data['item'],
    #                     'is_required': data['is_required'],
    #                     'value': value.lower(),
    #                     'product': product['pk']
    #                 })

    #     res = self.client.post(
    #         reverse('product-specification-list'), 
    #         data=product_specs, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )

    #     product_pks = list_to_str(list(dict.fromkeys([ data['product'] for data in res.data ])))
    #     products_res = self.client.get(
    #         reverse('product-list')+f'?pks={product_pks}', 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )

    #     self.assertEqual(products_res.data[0]['specifications'][0]['value'], 'blue')
    #     self.assertEqual(res.data[0]['value'], 'blue')
    #     self.assertEqual(res.status_code, 201)
    
    # def test_product_specs_create_errors(self):
    #     spec_values = [
    #         ['Blue', '34', 'Anasae'],
    #         ['Blue', '36', 'Anasae']
    #     ]
    #     product_specs = []
    #     for i, product in enumerate(self.products):
    #         if product['category'] and product['subcategory']:
    #             specifications = self.categories['subcategory_data']['product_specification']
    #             for spec in list(zip(specifications, spec_values[i])):
    #                 data, value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': '',
    #                     'is_required': data['is_required'],
    #                     'value': value.lower(),
    #                     'product': product['pk']
    #                 })
    #         else:
    #             specifications = self.categories['category']['product_specification']
    #             for spec in list(zip(specifications, spec_values[i])):
    #                 data, value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': '',
    #                     'is_required': data['is_required'],
    #                     'value': value.lower(),
    #                     'product': product['pk']
    #                 })

    #     res = self.client.post(
    #         reverse('product-specification-list'), 
    #         data=product_specs, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )

    #     self.assertEqual(res.status_code, 400)

    # def test_product_specs_create_permissions_failed(self):
    #     spec_values = [
    #         ['Blue', '34', 'Anasae'],
    #         ['Blue', '36', 'Anasae']
    #     ]
    #     product_specs = []
    #     for i, product in enumerate(self.products):
    #         if product['category'] and product['subcategory']:
    #             specifications = self.categories['subcategory_data']['product_specification']
    #             for spec in list(zip(specifications, spec_values[i])):
    #                 data, value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': data['item'],
    #                     'is_required': data['is_required'],
    #                     'value': value.lower(),
    #                 })
    #         else:
    #             specifications = self.categories['category']['product_specification']
    #             for spec in list(zip(specifications, spec_values[i])):
    #                 data, value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': data['item'],
    #                     'is_required': data['is_required'],
    #                     'value': value.lower(),
    #                 })

    #     res = self.client.post(
    #         reverse('product-specification-list'), 
    #         data=product_specs, 
    #         content_type='application/json',
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )

    #     self.assertEqual(res.status_code, 403)

    def test_product_specs_update(self):
        spec_values = [
            ['Blue', '34', 'Anasae'],
            ['Blue', '36', 'Anasae']
        ]
        product_specs = []
        for i, product in enumerate(self.products):
            if product['category'] and product['subcategory']:
                specifications = self.categories['subcategory_data']['product_specification']
                for spec in list(zip(specifications, spec_values[i])):
                    data, value = spec[0], spec[1]
                    product_specs.append({
                        'label': data['item'],
                        'is_required': data['is_required'],
                        'value': value.lower(),
                        'product': product['pk']
                    })
            else:
                specifications = self.categories['category']['product_specification']
                for spec in list(zip(specifications, spec_values[i])):
                    data, value = spec[0], spec[1]
                    product_specs.append({
                        'label': data['item'],
                        'is_required': data['is_required'],
                        'value': value.lower(),
                        'product': product['pk']
                    })

        specs_res = self.client.post(
            reverse('product-specification-list'), 
            data=product_specs, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        product_pks = list_to_str(list(dict.fromkeys([ data['product'] for data in specs_res.data ])))
        products_res = self.client.get(
            reverse('product-list')+f'?pks={product_pks}', 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        specs = [ spec for spec in specs_res.data if not spec['is_required'] ]
        spec_pk = specs[0]['pk']
        specs_res = self.client.put(
            reverse('product-specification-detail', kwargs={"pk":  spec_pk}), 
            data={"value": 'Fenty Beauty'}, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )