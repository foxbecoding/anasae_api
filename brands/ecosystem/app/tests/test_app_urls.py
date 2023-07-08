from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestBrandUrls(SimpleTestCase):
    
    def test_brand_list_url_resolves(self):
        url = reverse('brand-list')
        self.assertEqual(resolve(url).view_name, 'brand-list')
    
    def test_brand_detail_url_resolves(self):
        url = reverse('brand-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'brand-detail')