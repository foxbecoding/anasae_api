from brands.models import *
from brands.serializers import *
from users.ecosystem.methods import get_user_data
from users.models import User

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
    
    print(brand_data)
    return brand_data