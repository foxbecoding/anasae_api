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
        # Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        # Merchant_Store_Instances = MerchantStore.objects.filter(merchant_id=Merchant_Instance.id)
        # merchant_store_pks = [str(ms.id) for ms in Merchant_Store_Instances]

        # if request.method == 'POST':
        #     if 'merchant_store' not in request.data:
        #         return False
            
        #     store_pk = str(request.data['merchant_store'])

        #     if not MerchantStore.objects.filter(pk=store_pk).exists():
        #         return False 

        #     if store_pk not in merchant_store_pks:
        #         return False

        return True