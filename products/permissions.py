from rest_framework.permissions import BasePermission
from products.models import *
from products.serializers import ProductSerializer

class ProductPermission(BasePermission):
    message = "Access Denied!"   

    def has_object_permission(self, request, view, obj) -> bool:
        # allowed_methods = ['PATCH', 'GET']
        # if request.method in allowed_methods:
        #     if str(request.user.id) != str(obj['user_pk']):
        #         return False
        return True