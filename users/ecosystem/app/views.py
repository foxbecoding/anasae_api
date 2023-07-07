from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import *
from users.models import UserImage
from users.permissions import *
from users.ecosystem.methods import get_user_data

class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, UserPermission]
        if self.action == 'create':
            permission_classes = [UserPermission]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        Create_User_Serializer = CreateUserSerializer(data=request.data, context={'request': request})
        if not Create_User_Serializer.is_valid():
            return Response(Create_User_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        
        User_Instance = Create_User_Serializer.validated_data['user']
        data = get_user_data(User_Instance)
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'user_pk': pk})
        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_200_OK)

    @method_decorator(csrf_protect)
    def partial_update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'user_pk': pk})
        
        Edit_User_Serializer = EditUserSerializer(request.user, data=request.data, context={'request': request}, partial=True)
        if not Edit_User_Serializer.is_valid():
            return Response(Edit_User_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not Edit_User_Serializer.validated_data['password_changed']:
            Edit_User_Serializer.save()
            
            data = get_user_data(request.user)
            return Response(data, status=status.HTTP_202_ACCEPTED)
        
        logout(request)    
        return Response(None, status=status.HTTP_202_ACCEPTED)
    
class UserImageViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        user_id = str(request.user.id)
        is_User_Image = UserImage.objects.filter(user_id=user_id).exists()
        if is_User_Image:
            User_Image = UserImage.objects.get(user_id=user_id)
            # remove image from cdn maybe??? idk yet
            User_Image.delete()
        
        Create_User_Image_Serializer = CreateUserImageSerializer(data={'user': user_id}, context={ 'request': request })
        if not Create_User_Image_Serializer.is_valid():
            return Response(Create_User_Image_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_201_CREATED)
           
class UserAddressViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, UserAddressPermission]
        return [permission() for permission in permission_classes]
    
    @method_decorator(csrf_protect)
    def create(self, request):
        data = request.data
        data._mutable = True
        data['user'] = str(request.user.id)
        
        Create_User_Address_Serializer = CreateUserAddressSerializer(data=data)

        if not Create_User_Address_Serializer.is_valid():
            return Response(Create_User_Address_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        Create_User_Address_Serializer.save()
        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_201_CREATED)
          
    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'address_pk': pk})
        User_Address_Instance = UserAddress.objects.get(pk=pk)
        Edit_User_Address_Serializer = EditUserAddressSerializer(User_Address_Instance, data=request.data)

        if not Edit_User_Address_Serializer.is_valid():
            return Response(Edit_User_Address_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Edit_User_Address_Serializer.save()
        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_202_ACCEPTED)
        
    @method_decorator(csrf_protect)
    def destroy(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'address_pk': pk})
        User_Address_Instance = UserAddress.objects.get(pk=pk)
        User_Address_Instance.delete()
        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class UserPaymentMethodViewSet(viewsets.ViewSet):
    
    def get_permissions(self):
        permission_classes = [ IsAuthenticated, UserPaymentMethodPermission ]
        return [ permission() for permission in permission_classes ]

    def list(self, request):
        setup_intent_res = stripe.SetupIntent.create(
            customer=request.user.stripe_customer_id,
            payment_method_types=["card"],
        )
        return Response(setup_intent_res.client_secret, status=status.HTTP_200_OK)

    @method_decorator(csrf_protect)
    def create(self, request):
        self.check_object_permissions(request=request, obj={})
        payment_method_res = stripe.PaymentMethod.retrieve(id=request.data['payment_method_id'])

        data = {
            'user': str(request.user.id),
            'stripe_pm_id': payment_method_res.id
        }
        
        Create_User_Payment_Method_Serializer = CreateUserPaymentMethodSerializer(data=data)
        if not Create_User_Payment_Method_Serializer.is_valid():
            return Response(Create_User_Payment_Method_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        Create_User_Payment_Method_Serializer.save()
        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        # self.check_object_permissions(request=request, obj={'pk': pk})
        # Merchant_Payment_Method_Instance = MerchantPaymentMethod.objects.get(pk=str(pk))
        # Merchant_Payment_Method_Instance.delete()
        # stripe.PaymentMethod.detach(Merchant_Payment_Method_Instance.stripe_pm_id)
        # Merchant_Instance = Merchant.objects.get(user_id=str(request.user.id))
        # data = get_merchant_data(Merchant_Instance)
        # return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(None, status=status.HTTP_202_ACCEPTED)