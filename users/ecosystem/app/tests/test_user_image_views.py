from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from datetime import datetime
from utils.helpers import tmp_image

is_CSRF = True

class TestUserImageViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        self.date_time_str = '12/31/1990'

        user_data = {
            'first_name': "Anasae",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_str,
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        self.client.post(
            reverse('user-list'), 
            user_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        login_credentials = {
            'username': 'slugga',
            'password': '123456'
        }
    
        login_res = self.client.post(
            reverse('auth-log-in-list'), 
            login_credentials, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.user = login_res.data
        self.csrftoken = self.client.cookies['csrftoken'].value
        

    def test_user_image_create(self):
        request_data = {
            'image': tmp_image()
        }

        res = self.client.post(
            reverse('user-image-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertNotEqual(res.data['image'], None)
        self.assertEqual(res.status_code, 201)   

    def test_user_image_create_error(self):
        request_data = {
            'image': tmp_image('gif')
        }
        res = self.client.post(
            reverse('user-image-list'), 
            data=request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.assertEqual(res.status_code, 400)

    # This test uses the create method to update
    def test_user_image_update(self):
        create_image_request_data = {
            'image': tmp_image('png')
        }
        create_image_res = self.client.post(
            reverse('user-image-list'), 
            data=create_image_request_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        update_image_request_data = {
            'image': tmp_image('png')
        }
        update_image_res = self.client.post(
            reverse('user-image-list'),
            data=update_image_request_data,
            **{ 'HTTP_X_CSRFTOKEN': self.csrftoken }
        )
        self.assertEqual(create_image_res.status_code, 201)
        self.assertEqual(update_image_res.status_code, 201)