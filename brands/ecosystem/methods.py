from brands.models import *
from brands.serializers import *
from users.ecosystem.methods import get_user_data
from users.models import User

def get_brand_data(instance: Brand):
    brand_data = BrandSerializer(instance).data
    owner_pks = [ str(pk) for pk in brand_data['owners'] ]
    filter = [ 'pk','uid','first_name','last_name','display_name','username','image' ]
    brand_data['owners'] = [ 
        get_user_data(User.objects.get(pk=pk), filter=filter) 
        for pk in owner_pks 
    ]
    return brand_data