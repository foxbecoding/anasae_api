from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.serializers import *
from users.models import UserImage
from users.permissions import *
from users.ecosystem.methods import get_user_data
from utils.helpers import filter_obj, str_to_list
from datetime import datetime
from pprint import pprint
import stripe


class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated, UserPermission]
        if self.action == 'create':
            permission_classes = [UserPermission]
        elif self.action == 'list':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request):
        if str(request.user) == 'AnonymousUser':  
            return Response({'user': {}, 'status': False}, status=status.HTTP_200_OK)
        data = get_user_data(request.user)
        return Response({'user': data, 'status': True}, status=status.HTTP_200_OK)
        

    @method_decorator(csrf_protect)
    def create(self, request):
        request.data['date_of_birth'] = datetime.strptime(request.data['date_of_birth'], '%m/%d/%Y').date()
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
    
    def list(self, request):
        setup_intent_res = stripe.SetupIntent.create(
            customer=request.user.stripe_customer_id,
            payment_method_types=["card"],
        )
        return Response(setup_intent_res.client_secret, status=status.HTTP_200_OK)

    @method_decorator(csrf_protect)
    def create(self, request):
        data = request.data
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
    
    # def update(self, request, pk=None):
    #     if not UserPaymentMethod.objects.filter(pk=pk).filter(user_id=str(request.user.id)).exists():
    #         return Response(None, status=status.HTTP_403_FORBIDDEN)
        

    #     instance = UserPaymentMethod.objects.get(pk=pk)
    #     serializer_data = UserPaymentMethodSerializer(instance).data
    #     print(serializer_data)
    #     stripe.PaymentMethod.modify(
    #         serializer_data['stripe_pm_id']
    #     )
    #     return Response(None, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        pks = str_to_list(pk)
        instances =  UserPaymentMethod.objects.filter(pk__in=pks).filter(user=str(request.user.id))
        serialize_data = UserPaymentMethodSerializer(instances, many=True).data
        payment_methods = [ stripe.PaymentMethod.retrieve(data['stripe_pm_id']) for data in serialize_data ]
        return Response(payment_methods, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        self.check_object_permissions(request=request, obj={'payment_method_pk': pk})
        User_Payment_Method_Instance = UserPaymentMethod.objects.get(pk=str(pk))
        stripe.PaymentMethod.detach(User_Payment_Method_Instance.stripe_pm_id)
        User_Payment_Method_Instance.delete()
        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_202_ACCEPTED)
    
class UserBillingAddressViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [ IsAuthenticated ]
        return [ permission() for permission in permission_classes ]
    
    def create(self, request):
        request.data['user'] = str(request.user.id)
        serializer = CreateUserBillingAddressSerializer(data=request.data)
        
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        
        payment_method_instance = UserPaymentMethod.objects.get(pk=request.data['payment_method'])
        payment_method_serializer_data = UserPaymentMethodSerializer(payment_method_instance).data
        
        address_instance = UserAddress.objects.get(pk=request.data['address'])
        address_serializer_data = UserAddressSerializer(address_instance).data

        stripe.PaymentMethod.modify(
            payment_method_serializer_data['stripe_pm_id'],
            billing_details = {
                "address": {
                    "city": address_serializer_data['city'],
                    "country": address_serializer_data['country'],
                    "line1": address_serializer_data['street_address'],
                    "line2": address_serializer_data['street_address_ext'],
                    "postal_code": address_serializer_data['postal_code'],
                    "state": address_serializer_data['state']
                },
                "name": address_serializer_data['full_name'],
                "phone": address_serializer_data['phone_number']
            },
        )

        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_201_CREATED)

class UserGenderViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [ AllowAny ]
        return [ permission() for permission in permission_classes ]

    def list(self, request):
        instance = UserGender.objects.all()
        serializer = UserGenderSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileViewSet(viewsets.ViewSet):
    lookup_field = 'uid'
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, uid=None):
        if not User.objects.filter(uid=uid).exists(): return Response(None, status=status.HTTP_404_NOT_FOUND)
        
        instance = User.objects.get(uid=uid)
        user_serializer = UserSerializer(instance)
        user_followers_ins = UserFollower.objects.filter(pk__in=user_serializer.data['followers'])
        user_follower_serializer = UserFollowerSerializer(user_followers_ins, many=True)
        user_followers = [ str(user['follower']) for user in user_follower_serializer.data ]
        user_data = get_user_data(instance)
        
        if str(instance.id) == str(request.user.id):
            user_data['isOwner'] = True
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            filter = ["pk", "uid", "first_name", "last_name", "username", "image", "followers", "display_name"]
            filtered_user_data = filter_obj(user_data, filter=filter)
            filtered_user_data['isFollowing'] = str(request.user.id) in user_followers
            filtered_user_data['isOwner'] = False
            return Response(filtered_user_data, status=status.HTTP_200_OK)

class UserFollowerViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [ permission() for permission in permission_classes ]

    @method_decorator(csrf_protect)
    def create(self, request):
        request.data['follower'] = str(request.user.id)
        create_serializer = CreateUserFollowerSerializer(data=request.data)
        if not create_serializer.is_valid():
            return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = get_user_data(request.user)
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        return Response(None, status=status.HTTP_200_OK)
    
    @method_decorator(csrf_protect)
    def destroy(self, request, pk=None):
        instance = UserFollower.objects.filter(user_id=pk).filter(follower_id=str(request.user.id)).first()
        instance.delete()
        return Response(None, status=status.HTTP_202_ACCEPTED)