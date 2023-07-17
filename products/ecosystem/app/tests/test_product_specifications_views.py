from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from categories.ecosystem.methods import test_categories
from datetime import datetime

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

    def test_product_specs_create(self):
        pass    
    # spec_values = data['spec_values']
    #         product_specs = []
    #         if product['category'] and product['subcategory']:
    #             specifications = self.categories['subcategory_data']['product_specification']
    #             for spec in list(zip(specifications, spec_values)):
    #                 spec_data, spec_value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': spec_data['item'],
    #                     'is_required': spec_data['is_required'],
    #                     'value': spec_value,
    #                 })
    #         else:
    #             specifications = self.categories['category']['product_specification']
    #             for spec in list(zip(specifications, spec_values)):
    #                 spec_data, spec_value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': spec_data['item'],
    #                     'is_required': spec_data['is_required'],
    #                     'value': spec_value,
    #                 })

    #         product['specifications'] = product_specs
    #         product['images'] = [tmp_image() for x in range(7)]