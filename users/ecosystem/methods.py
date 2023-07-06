from users.serializers import *
from users.models import *

def get_user_data(instance: User):
    User_Serializer = UserSerializer(instance)
    user_data = User_Serializer.data
    User_Login_Instances = UserLogin.objects.filter(pk__in=user_data['logins'])
    User_Account_Login_Serializer = UserLoginSerializer(User_Login_Instances, many=True)
    User_Address_Instance = UserAddress.objects.filter(pk__in=user_data['addresses'])
    User_Address_Serializer = UserAddressSerializer(User_Address_Instance, many=True)

    if UserImage.objects.filter(pk=user_data['image']).exists():
        User_Image_Instance = UserImage.objects.get(pk=user_data['image'])
        user_data['image'] = UserImageSerializer(User_Image_Instance)

    data = {
        'pk': user_data['pk'],
        'uid': user_data['uid'],
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'display_name': user_data['display_name'],
        'username': user_data['username'],
        'logins': User_Account_Login_Serializer.data,
        'addresses': User_Address_Serializer.data,
        'image': user_data['image']
    }
    
    return data