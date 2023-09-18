from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestCategoryUrls(SimpleTestCase):
    
    def test_category_list_url_resolves(self):
        url = reverse('category-list')
        self.assertEqual(resolve(url).view_name, 'category-list')
    
    def test_category_product_specification_detail_url_resolves(self):
        url = reverse('category-product-specification-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'category-product-specification-detail')
    