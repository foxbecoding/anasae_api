from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestProductUrls(SimpleTestCase):
    
    def test_product_list_url_resolves(self):
        url = reverse('product-list')
        self.assertEqual(resolve(url).view_name, 'product-list')
    
    def test_product_detail_url_resolves(self):
        url = reverse('product-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-detail')

class TestProductPriceUrls(SimpleTestCase):
    
    def test_product_price_list_url_resolves(self):
        url = reverse('product-price-list')
        self.assertEqual(resolve(url).view_name, 'product-price-list')
    
    def test_product_price_detail_url_resolves(self):
        url = reverse('product-price-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-price-detail')