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
        print(self.products)
    
  