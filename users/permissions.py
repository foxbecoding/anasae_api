from rest_framework.permissions import BasePermission
from users.models import *
from users.serializers import UserSerializer

class UserPermission(BasePermission):
    message = "Access Denied!"   

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == 'POST':
            if 'gender' not in request.data:
                return False
            
            gender_pk = request.data['gender']
            if not UserGender.objects.filter(pk=gender_pk).exists():  
                return False
        return True

# class UserImagePermission(BasePermission):
#     message = "Access Denied!"   

#     def has_permission(self, request, view):
#         User_Serializer = UserSerializer(request.user) 
#         user_profile_pks = (str(profile) for profile in User_Serializer.data['profiles'])  
        
#         if str(request.data['user_profile']) not in user_profile_pks:
#             return False     
#         return True

# class UserAddressPermission(BasePermission):
#     message = "Access Denied!"   

#     def has_permission(self, request, view):
#         SAFE_METHODS = ('POST', 'PUT', 'DELETE')
#         if request.method in SAFE_METHODS:
#             return True
#         return False
    
#     def has_object_permission(self, request, view, obj):
#         User_Serializer = UserSerializer(request.user) 
#         user_address_pks = (str(address) for address in User_Serializer.data['addresses'])

#         if str(obj['address_pk']) not in user_address_pks:
#             return False
#         return True