from users.serializers import *
from users.models import *

def get_user_Data(instance: User):
    User_Serializer = UserSerializer(instance)
    User_Data = User_Serializer.data
    User_Login_Instances = UserLogin.objects.filter(pk__in=User_Data['logins'])
    User_Account_Login_Serializer = UserLoginSerializer(User_Login_Instances, many=True)
    
    user_logins = [
        {
            'pk': login['pk'],
            'logged_in_date': login['created']
        }
        for login in User_Account_Login_Serializer.data
    ]

    User_Address_Instance = UserAddress.objects.filter(pk__in=User_Data['addresses'])
    User_Address_Serializer = UserAddressSerializer(User_Address_Instance, many=True)

    data = {
        'pk': User_Data['pk'],
        'uid': User_Data['uid'],
        'first_name': User_Data['first_name'],
        'last_name': User_Data['last_name'],
        'email': User_Data['email'],
        'username': User_Data['username'],
        'logins': user_logins,
        'addresses': User_Address_Serializer.data
    }
    
    return data