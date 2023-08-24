from users.serializers import *
from users.models import *
from brands.models import *
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
    User_Owned_Brands = BrandOwner.objects.filter(user=user_data['pk'])
    brands = []
    if(len(User_Owned_Brands) > 0):
        User_Owned_Brands_Serializer = BrandOwnerSerializer(User_Owned_Brands, many=True)
        owned_brands_pks = [ owned_brand['pk'] for owned_brand in User_Owned_Brands_Serializer.data ]
        brands = get_owner_brands(owned_brands_pks)

    if UserImage.objects.filter(pk=user_data['image']).exists():
        User_Image_Instance = UserImage.objects.get(pk=user_data['image'])
        user_data['image'] = UserImageSerializer(User_Image_Instance).data

    data = {
        'addresses': User_Address_Serializer.data,
        'brands': brands,
        'display_name': user_data['display_name'],
        'email': user_data['email'],
        'first_name': user_data['first_name'],
        'image': user_data['image'],
        'last_name': user_data['last_name'],
        'logins': User_Account_Login_Serializer.data,
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

def get_owner_data(instance: User):
    filter = [ 'pk','uid','first_name','last_name','display_name','username','image' ]
    return get_user_data(instance, filter=filter)

def get_brand_data(instance: Brand):
    brand_data = BrandSerializer(instance).data
    Brand_Owner_Instances = BrandOwner.objects.filter(pk__in=brand_data['owners'])
    brand_owner_data = BrandOwnerSerializer(Brand_Owner_Instances, many=True).data
    owner_pks = [ str(owner['user']) for owner in brand_owner_data ]
    User_Instances = User.objects.filter(pk__in=owner_pks)
    brand_data['owners'] = [ get_owner_data(instance) for instance in User_Instances ]
    
    is_brand_logo = BrandLogo.objects.filter(pk=brand_data['logo']).exists()
    if is_brand_logo:
        Brand_Logo_Instance = BrandLogo.objects.get(pk=brand_data['logo'])
        brand_data['logo'] = BrandLogoSerializer(Brand_Logo_Instance).data
    
    brand_data['followers'] = len(brand_data['followers'])
    
    return brand_data

def get_owner_brands(pks = []):
    if len(pks) == 0: return pks
    brand_ins = Brand.objects.filter(pk__in=pks)
    return [ get_brand_data(ins) for ins in brand_ins]