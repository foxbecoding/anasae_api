from rest_framework.permissions import BasePermission
from brands.models import *

class BrandPermission(BasePermission):
    
    message = "Access Denied!" 

    def has_object_permission(self, request, view, obj) -> bool:
        # pk = obj['pk']
        
        # if not Brand.objects.filter(user_id=str(request.user.id)).exists():
        #     return False
        
        # if not Merchant.objects.filter(pk=pk).exists():
        #     return False
        
        # Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        # if str(Merchant_Instance.id) != str(pk):
        #     return False
        
        return True