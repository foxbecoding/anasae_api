from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from cart.models import *
from cart.serializers import *

class CartViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        cart_ins = Cart.objects.get(user_id=str(request.user.id))
        serialized_cart_data =  CartSerializer(cart_ins).data
        cart_items_ins = CartItem.objects.filter(pk__in=serialized_cart_data['items'])
        serialized_cart_data['items'] = CartItemSerializer(cart_items_ins, many=True).data
        return Response(serialized_cart_data, status=status.HTTP_200_OK)
    
class CartItemViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        return Response(None, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        return Response(None, status=status.HTTP_200_OK)