from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, UserGender
from datetime import datetime
from pprint import pprint

is_CSRF = True

class TestUserGenderViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

    def test_user_gender_retrieve(self):
        res = self.client.get(
            reverse('user-gender-list')
        )
        
        self.assertEqual(res.data['gender'], 'Male')
        self.assertEqual(res.status_code, 200)