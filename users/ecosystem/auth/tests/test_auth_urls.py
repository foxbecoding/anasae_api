from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestAccountSignUpUrls(SimpleTestCase):
    
    def test_account_sign_up_list_url_resolves(self):
        url = reverse('account-sign-up-list')
        self.assertEqual(resolve(url).view_name, 'account-sign-up-list')

    # def test_user_sign_up_detail_url_resolves(self):
    #     url = reverse('user-sign-up-detail', kwargs={'pk': 1})
    #     self.assertEqual(resolve(url).view_name, 'user-sign-up-detail')

class TestAccountLogInUrls(SimpleTestCase):
    
    def test_account_log_in_list_url_resolves(self):
        url = reverse('account-log-in-list')
        self.assertEqual(resolve(url).view_name, 'account-log-in-list')

class TestAccountLogOutUrls(SimpleTestCase):
    
    def test_account_log_out_list_url_resolves(self):
        url = reverse('account-log-out-list')
        self.assertEqual(resolve(url).view_name, 'account-log-out-list')