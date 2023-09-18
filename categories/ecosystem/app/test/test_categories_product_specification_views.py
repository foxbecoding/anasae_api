from django.test import TestCase, Client
from django.urls import reverse
from categories.ecosystem.methods import test_categories
from pprint import pprint

is_CSRF = True

class TestCategoryProductSpecificationViewSet(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.categories = test_categories()

    def test_category_product_specification_retrieve(self):
        pk = self.categories['category_data']['product_specification_id']
        res = self.client.get(reverse('category-product-specification-detail', kwargs={'pk': pk}))
        self.assertGreater(len(res.data), 0)
        self.assertEqual(res.status_code, 200)
