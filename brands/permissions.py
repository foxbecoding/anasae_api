from rest_framework.permissions import BasePermission
from brands.models import *

class BrandPermission(BasePermission):
    
    message = "Access Denied!" 

    def has_object_permission(self, request, view, obj) -> bool:
        brand_pk = obj['brand_pk']
        user_pk = str(request.user.id)
    
        if not Brand.objects.filter(pk=brand_pk).filter(owners__in=user_pk).exists():
            return False
        
        return True