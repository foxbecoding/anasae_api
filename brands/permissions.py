from rest_framework.permissions import BasePermission
from brands.models import *

class BrandPermission(BasePermission):
    
    message = "Access Denied!" 

    def has_object_permission(self, request, view, obj) -> bool:
        brand_pk = obj['brand_pk']
        user_pk = str(request.user.id)
    
        if not BrandOwner.objects.filter(brand_id=brand_pk).filter(owner_id=user_pk).exists():
            return False
        
        return True