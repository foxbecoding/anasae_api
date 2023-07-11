from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestCategoryUrls(SimpleTestCase):
    
    def test_category_list_url_resolves(self):
        url = reverse('category-list')
        self.assertEqual(resolve(url).view_name, 'category-list')
    