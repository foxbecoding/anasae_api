from rest_framework.permissions import BasePermission
from users.models import *
from users.serializers import UserSerializer

class UserPermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        if request.method == 'POST':
            if 'gender' not in request.data:
                return False
            
            gender_pk = request.data['gender']
            if not UserGender.objects.filter(pk=gender_pk).exists():  
                return False
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        allowed_methods = ['PATCH', 'GET']
        if request.method in allowed_methods:
            if str(request.user.id) != str(obj['user_pk']):
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

class UserAddressPermission(BasePermission):
    message = "Access Denied!"   
    
    def has_object_permission(self, request, view, obj):
        User_Serializer = UserSerializer(request.user) 
        user_address_pks = (str(address) for address in User_Serializer.data['addresses'])

        if str(obj['address_pk']) not in user_address_pks:
            return False
        return True
    
class UserPaymentMethodPermission(BasePermission):
    
    message = "Access Denied!"

    # def has_permission(self, request, view) -> bool:
    #     return Merchant.objects.filter(user_id=str(request.user.id)).exists() 
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            payment_method_pk = obj['payment_method_pk']
            
            is_payment_method = UserPaymentMethod.objects.filter(pk=payment_method_pk).exists()
            if not is_payment_method:
                return False
            
            User_Payment_Method_Instance = UserPaymentMethod.objects.get(pk=payment_method_pk)
            is_user_match = str(request.user.id) == str(User_Payment_Method_Instance.user_id)
            if not is_user_match:
                return False

        return True