from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestBrandUrls(SimpleTestCase):
    
    def test_brand_list_url_resolves(self):
        url = reverse('brand-list')
        self.assertEqual(resolve(url).view_name, 'brand-list')
    
    def test_brand_detail_url_resolves(self):
        url = reverse('brand-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'brand-detail')

class TestBrandLogoUrls(SimpleTestCase):
    
    def test_brand_logo_list_url_resolves(self):
        url = reverse('brand-logo-list')
        self.assertEqual(resolve(url).view_name, 'brand-logo-list')

class TestBrandOwnerUrls(SimpleTestCase):
    
    def test_brand_owner_list_url_resolves(self):
        url = reverse('brand-owner-list')
        self.assertEqual(resolve(url).view_name, 'brand-owner-list')

    def test_brand_owner_detail_url_resolves(self):
        url = reverse('brand-owner-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'brand-owner-detail')

class TestBrandFollowerUrls(SimpleTestCase):
    
    def test_brand_follower_list_url_resolves(self):
        url = reverse('brand-follower-list')
        self.assertEqual(resolve(url).view_name, 'brand-follower-list')