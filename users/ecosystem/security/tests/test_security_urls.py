from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestSecurityUrls(SimpleTestCase):
    
    def test_security_list_url_resolves(self):
        url = reverse('x-fct-list')
        self.assertEqual(resolve(url).view_name, 'x-fct-list')