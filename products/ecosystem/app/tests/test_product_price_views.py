from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from categories.ecosystem.methods import test_categories
from products.ecosystem.methods import test_products
from datetime import datetime

is_CSRF = True

class TestProductPriceViewSet(TestCase):
 
    def setUp(self):
        self.categories = test_categories()
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.products = test_products(self.categories)

    def test_product_price_create(self):
        request_data = []
        for product in self.products:
            request_data.append({
                'price': 2999,
                'product': product['pk']
            })

        res = self.client.post(
            reverse('product-price-list'), 
            data=request_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ) 