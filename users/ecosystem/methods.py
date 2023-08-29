from users.serializers import *
from users.models import *
from brands.models import BrandOwner
from brands.serializers import * 

def get_user_data(instance: User, filter = []):
    User_Serializer = UserSerializer(instance)
    user_data = User_Serializer.data
    User_Login_Instances = UserLogin.objects.filter(pk__in=user_data['logins'])
    User_Account_Login_Serializer = UserLoginSerializer(User_Login_Instances, many=True)
    User_Address_Instance = UserAddress.objects.filter(pk__in=user_data['addresses'])
    User_Address_Serializer = UserAddressSerializer(User_Address_Instance, many=True)
    User_Payment_Method_Instance = UserPaymentMethod.objects.filter(pk__in=user_data['payment_methods'])
    User_Payment_Method_Serializer = UserPaymentMethodSerializer(User_Payment_Method_Instance, many=True)

    if UserImage.objects.filter(pk=user_data['image']).exists():
        User_Image_Instance = UserImage.objects.get(pk=user_data['image'])
        user_data['image'] = UserImageSerializer(User_Image_Instance).data

    data = {
        'addresses': User_Address_Serializer.data,
        'display_name': user_data['display_name'],
        'email': user_data['email'],
        'first_name': user_data['first_name'],
        'followers': len(user_data['followers']),
        'image': user_data['image'],
        'last_name': user_data['last_name'],
        'logins': User_Account_Login_Serializer.data,
        'owned_brands': user_data['owned_brands'],
        'payment_methods': User_Payment_Method_Serializer.data,
        'pk': user_data['pk'],
        'stripe_customer_id': user_data['stripe_customer_id'],
        'uid': user_data['uid'],
        'username': user_data['username']
    }

    if len(filter) > 0:
        newDict = dict()
        for (key, value) in data.items():
            if key in filter:
                newDict[key] = value
        data = newDict
    
    return data

