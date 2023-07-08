from brands.models import *
from brands.serializers import *
from users.ecosystem.methods import get_user_data
from users.models import User

def get_brand_data(instance: Brand):
    brand_data = BrandSerializer(instance).data
    Brand_Owner_Instances = BrandOwner.objects.filter(pk__in=brand_data['owners'])
    brand_owner_data = BrandOwnerSerializer(Brand_Owner_Instances, many=True).data
    filter = [ 'pk','uid','first_name','last_name','display_name','username','image' ]
    brand_data['owners'] = [ 
        get_user_data(User.objects.get(pk=owner['user']), filter=filter) 
        for owner in brand_owner_data 
    ]
    return brand_data