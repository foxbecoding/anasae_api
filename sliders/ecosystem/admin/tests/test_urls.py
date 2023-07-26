from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestAdminSliderUrls(SimpleTestCase):
    
    def test_admin_slider_list_url_resolves(self):
        url = reverse('admin-slider-list')
        self.assertEqual(resolve(url).view_name, 'admin-slider-list')

class TestAdminSliderImageUrls(SimpleTestCase):
    
    def test_admin_slider_image_list_url_resolves(self):
        url = reverse('admin-slider-image-list')
        self.assertEqual(resolve(url).view_name, 'admin-slider-image-list')