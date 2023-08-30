from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from pprint import pprint

is_CSRF = True

class TestUserProfileViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        self.date_time_str = '12/31/1990'

        user_data = {
            'first_name': "Lavell",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_str,
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        self.user = self.client.post(
            reverse('user-list'), 
            user_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        ).data


    def test_user_profile_retrieve_logged_in(self):
        #User Login
        login_credentials = {
            'username': 'slugga',
            'password': '123456'
        }
    
        #Get response data
        auth_res = self.client.post(
            reverse('auth-log-in-list'), 
            login_credentials, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        user = auth_res.data
        self.csrftoken = self.client.cookies['csrftoken'].value

        profile_res = self.client.get(
            reverse('user-profile-detail', kwargs={ 'uid': user['uid'] }),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertTrue(profile_res.data['isOwner'])
        self.assertEquals(profile_res.status_code, 200)

    def test_user_profile_retrieve_not_logged_in(self):
        
        profile_res = self.client.get(
            reverse('user-profile-detail', kwargs={ 'uid': self.user['uid'] }),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertFalse(profile_res.data['isOwner'])
        self.assertEquals(profile_res.status_code, 200)
    
    def test_user_profile_retrieve_not_found(self):
        
        profile_res = self.client.get(
            reverse('user-profile-detail', kwargs={ 'uid': 'snd98h3' }),
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.assertEquals(profile_res.status_code, 404)