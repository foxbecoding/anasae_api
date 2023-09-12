from django.test import TestCase, Client
from django.urls import reverse
from categories.ecosystem.methods import test_categories
from pprint import pprint

is_CSRF = True

class TestCategoryViewSet(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.categories = test_categories()

    def test_category_list(self):
        res = self.client.get(reverse('category-list'))
        self.assertGreater(len(res.data), 0)
        self.assertEqual(res.status_code, 200)
