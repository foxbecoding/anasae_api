from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUserUrls(SimpleTestCase):
    
    def test_user_list_url_resolves(self):
        url = reverse('user-list')
        self.assertEqual(resolve(url).view_name, 'user-list')
    
    def test_user_detail_url_resolves(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'user-detail')