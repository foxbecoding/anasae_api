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

class TestAuthForgotPasswordUrls(SimpleTestCase):
    
    def test_auth_log_out_list_url_resolves(self):
        url = reverse('auth-forgot-password-list')
        self.assertEqual(resolve(url).view_name, 'auth-forgot-password-list')

class TestAuthValidateUrls(SimpleTestCase):
    
    def test_auth_validate_list_url_resolves(self):
        url = reverse('auth-validate-list')
        self.assertEqual(resolve(url).view_name, 'auth-validate-list')

class TestAuthValidateDetailsUrls(SimpleTestCase):
    
    def test_auth_validate_details_list_url_resolves(self):
        url = reverse('auth-validate-details-list')
        self.assertEqual(resolve(url).view_name, 'auth-validate-details-list')

class TestAuthValidatePasswordUrls(SimpleTestCase):
    
    def test_auth_validate_details_list_url_resolves(self):
        url = reverse('auth-validate-password-list')
        self.assertEqual(resolve(url).view_name, 'auth-validate-password-list')

class TestVerifyEmailUrls(SimpleTestCase):
    
    def test_auth_verify_email_list_url_resolves(self):
        url = reverse('auth-verify-email-list')
        self.assertEqual(resolve(url).view_name, 'auth-verify-email-list')
    
    def test_auth_verify_email_detail_url_resolves(self):
        url = reverse('auth-verify-email-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'auth-verify-email-detail')