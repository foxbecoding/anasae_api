from rest_framework.permissions import BasePermission
from products.models import *
from products.serializers import ProductSerializer
from brands.models import BrandOwner
from brands.serializers import BrandOwnerSerializer


class ProductPermission(BasePermission):
    message = "Access Denied!"   

    def has_object_permission(self, request, view, obj) -> bool:
        if 'brand' not in request.data: return False 
    
        brand_pk = obj['brand']
        Brand_Owner_Instances = BrandOwner.objects.filter(user_id=str(request.user.id))
        brand_owner_data = BrandOwnerSerializer(Brand_Owner_Instances, many=True)
        print(brand_owner_data)
        # allowed_methods = ['PATCH', 'GET']
        # if request.method in allowed_methods:
        #     if str(request.user.id) != str(obj['user_pk']):
        #         return False
        return True