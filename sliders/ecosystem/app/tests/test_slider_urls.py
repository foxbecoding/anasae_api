from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestSliderUrls(SimpleTestCase):
    
    def test_slider_detail_url_resolves(self):
        url = reverse('slider-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'slider-detail')
