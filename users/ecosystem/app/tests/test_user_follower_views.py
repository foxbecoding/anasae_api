from django.test import TestCase, Client
from django.urls import reverse
from users.models import UserGender
from pprint import pprint

is_CSRF = True

class TestUserFollowerViewSet(TestCase):
    
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

        self.client.post(
            reverse('user-list'), 
            user_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        #User Login
        login_credentials = {
            'username': 'slugga',
            'password': '123456'
        }
    
        #Get response data
        res = self.client.post(
            reverse('auth-log-in-list'), 
            login_credentials, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        self.user = res.data
        self.csrftoken = self.client.cookies['csrftoken'].value

        user_data = {
            'first_name': "test",
            'last_name': 'test',
            'email': 'test@gmail.com',
            'username': 'test',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': self.date_time_str,
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        res2 = self.client.post(
            reverse('user-list'), 
            user_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        self.user2 = res2.data

    def test_user_follower_create(self):
        # pprint(self.user)
        # pprint(self.user2)
        post_data = {
            'user': self.user2['pk']
        }
        res1 = self.client.post(
            reverse('user-follower-list'), 
            post_data, 
            content_type='application/json',
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        print(self.user2['uid'])
        res2 = self.client.get(
            reverse('user-profile-detail', kwargs={'uid': self.user2['uid']}),
            content_type='application/json'
        )

        pprint(res2.data)
        print(res2.status_code)
        self.assertEquals(res1.data['followed_users'], 1)
        self.assertEquals(res1.status_code, 201)