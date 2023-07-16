from django.test import Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime

def test_products(categories):
    client = Client(enforce_csrf_checks=True)
    client.get(reverse('x-fct-list'))
    csrftoken = client.cookies['csrftoken'].value
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

    client.post(
        reverse('user-list'), 
        user_data, 
        **{'HTTP_X_CSRFTOKEN': csrftoken}
    )

    login_credentials = {
        'username': 'slugga',
        'password': '123456'
    }

    login_res = client.post(
        reverse('auth-log-in-list'), 
        login_credentials, 
        **{'HTTP_X_CSRFTOKEN': csrftoken}
    )
    user = login_res.data
    csrftoken = client.cookies['csrftoken'].value

    brand_request_data = { 
        'name': 'ANASAE',
        'bio': 'ANASAE has all of the essentials for all of your needs.  Shop with us today!',
    }

    brand_res = client.post(
        reverse('brand-list'), 
        data=brand_request_data, 
        **{'HTTP_X_CSRFTOKEN': csrftoken}
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
            'category': categories['category_data']['pk'],
            'subcategory': categories['subcategory_data']['pk'],
            'title': data['title'],
            'description': data['description'],
            'quantity': 20,
            'sku': None,
            'isbn': None
        }

        request_data.append(product)
    
    res = client.post(
            reverse('product-list'), 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': csrftoken}
        ) 
    return res.data