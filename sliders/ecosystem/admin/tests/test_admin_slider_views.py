from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from users.models import UserGender
from users.models import User

is_CSRF = True

class TestAdminSliderViewSet(TestCase):
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=is_CSRF)
        self.client.get(reverse('x-fct-list'))
        self.csrftoken = self.client.cookies['csrftoken'].value
        self.User_Gender_Instance = UserGender.objects.create(gender = 'Male')
        self.User_Gender_Instance.save()

        date_time_str = '12/31/1990'
        date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y')

        user_data = {
            'first_name': "Lavell",
            'last_name': 'Fox',
            'email': 'slugga@gmail.com',
            'username': 'slugga',
            'password': '123456',
            'confirm_password': '123456',
            'date_of_birth': date_time_obj.date(),
            'agreed_to_toa': True,
            'gender': self.User_Gender_Instance.id
        }

        user = self.client.post(
            reverse('user-list'), 
            user_data, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )

        user_instance = User.objects.get(pk=user.data['pk'])
        user_instance.is_staff = True
        user_instance.save()

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

    def test_admin_slider_create(self):
        res = self.client.post(
            reverse('admin-slider-list'), 
            {'name': 'Home page slider'}, 
            **{'HTTP_X_CSRFTOKEN': self.csrftoken}
        )
        
        self.assertEqual(res.data['name'], 'Home page slider')      
        self.assertEqual(res.status_code, 201)      