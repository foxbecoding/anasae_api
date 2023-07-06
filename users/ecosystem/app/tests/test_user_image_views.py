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

        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        user_data = {
            'first_name': "Anasae",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        self.client.post(
            reverse('user-list'), 
            user_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        login_credentials = {
            'username': 'slugga',
            'password': '123456'
        }
    
        login_res = self.client.post(
            reverse('auth-log-in-list'), 
            login_credentials, 
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

        # print(res.data)

        # self.assertNotEqual(res.data['profiles'][0]['image'], None)
        # self.assertEqual(res.status_code, 201)   

    # def test_mpa_user_profile_image_create_error(self):
    #     request_data = {
    #         'user_profile': self.user['profiles'][0],
    #         'image': tmp_image('gif')
    #     }
    #     res = self.client.post(
    #         reverse('mpa-user-profile-image-list'), 
    #         data=request_data, 
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )
    #     self.assertEqual(res.status_code, 400)
    
    # def test_mpa_user_profile_image_create_permissions_failed(self):
    #     request_data = {
    #         'user_profile': 1111,
    #         'image': tmp_image('png')
    #     }
    #     res = self.client.post(
    #         reverse('mpa-user-profile-image-list'), 
    #         data=request_data, 
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )
    #     self.assertEqual(res.status_code, 403)

    # # This test uses the create method to update
    # def test_mpa_user_profile_image_update(self):
    #     create_image_request_data = {
    #         'user_profile': self.user['profiles'][0],
    #         'image': tmp_image('png')
    #     }
    #     create_image_res = self.client.post(
    #         reverse('mpa-user-profile-image-list'), 
    #         data=create_image_request_data, 
    #         **{'HTTP_X_CSRFTOKEN': self.csrftoken}
    #     )
    #     update_image_request_data = {
    #         'user_profile': self.user['profiles'][0],
    #         'image': tmp_image('png')
    #     }
    #     update_image_res = self.client.post(
    #         reverse('mpa-user-profile-image-list'),
    #         data=update_image_request_data,
    #         **{ 'HTTP_X_CSRFTOKEN': self.csrftoken }
    #     )
    #     self.assertEqual(create_image_res.status_code, 201)
    #     self.assertEqual(update_image_res.status_code, 201)