from django.test import TestCase, Client
from django.urls import reverse

class TestForceCSRFViewSet(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('x-fct-list')

    def test_force_csrf_list(self):
        self.client.get(self.list_url)
        self.assertIn('csrftoken', self.client.cookies)
    