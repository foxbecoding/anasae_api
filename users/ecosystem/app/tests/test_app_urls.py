from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUserUrls(SimpleTestCase):
    
    def test_user_list_url_resolves(self):
        url = reverse('user-list')
        self.assertEqual(resolve(url).view_name, 'user-list')
    
    def test_user_detail_url_resolves(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'user-detail')

class TestUserImageUrls(SimpleTestCase):

    def test_user_image_list_url_resolves(self):
        url = reverse('user-image-list')
        self.assertEqual(resolve(url).view_name, 'user-image-list')

class TestUserAddressUrls(SimpleTestCase):

    def test_user_address_list_url_resolves(self):
        url = reverse('user-address-list')
        self.assertEqual(resolve(url).view_name, 'user-address-list')
    
    def test_user_address_detail_url_resolves(self):
        url = reverse('user-address-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'user-address-detail')

class TestUserPaymentMethodUrls(SimpleTestCase):

    def test_user_payment_method_list_url_resolves(self):
        url = reverse('user-payment-method-list')
        self.assertEqual(resolve(url).view_name, 'user-payment-method-list')
    
    def test_user_payment_method_detail_url_resolves(self):
        url = reverse('user-payment-method-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'user-payment-method-detail')