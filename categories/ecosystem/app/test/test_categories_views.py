from django.test import TestCase, Client
from django.urls import reverse
from categories.ecosystem.methods import test_categories

is_CSRF = True

class TestCategoryViewSet(TestCase):
 
    def setUp(self):
        self.categories = test_categories()

    def test_category_list(self):
        print(self.categories)