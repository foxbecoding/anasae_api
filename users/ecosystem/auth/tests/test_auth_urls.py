from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestAuthLogInUrls(SimpleTestCase):
    
    def test_auth_log_in_list_url_resolves(self):
        url = reverse('auth-log-in-list')
        self.assertEqual(resolve(url).view_name, 'auth-log-in-list')

class TestAuthLogOutUrls(SimpleTestCase):
    
    def test_auth_log_out_list_url_resolves(self):
        url = reverse('auth-log-out-list')
        self.assertEqual(resolve(url).view_name, 'auth-log-out-list')