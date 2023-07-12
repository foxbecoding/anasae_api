from rest_framework.permissions import BasePermission
from products.models import *
from products.serializers import ProductSerializer
from brands.models import BrandOwner
from brands.serializers import BrandOwnerSerializer


class ProductPermission(BasePermission):
    message = "Access Denied!"   

    def has_object_permission(self, request, view, obj) -> bool:
        if 'brand' not in request.data: return False 
    
        brand_pk = str(obj['brand_pk'])
        Brand_Owner_Instances = BrandOwner.objects.filter(user_id=str(request.user.id))
        brand_owner_data = BrandOwnerSerializer(Brand_Owner_Instances, many=True).data
        brand_pks = [ str(brand['brand']) for brand in brand_owner_data ]
        
        if brand_pk not in brand_pks: return False
        
        return True