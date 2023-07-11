from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product
from categories.ecosystem.methods import test_categories

is_CSRF = True

class TestProductViewSet(TestCase):
 
    def setUp(self):
        self.categories = test_categories()

    def test_product_list(self):
        print(self.categories)