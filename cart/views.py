from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from cart.models import *
from cart.serializers import *
from products.ecosystem.classes import ProductListingPageView
from pprint import pprint

class CartViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        cart = getCart(request)
        return Response(cart, status=status.HTTP_200_OK)
    
class CartItemViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @method_decorator(csrf_protect)
    def create(self, request):
        serializer = CreateCartItemSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        cart = getCart(request)
        return Response(cart, status=status.HTTP_201_CREATED)

    @method_decorator(csrf_protect)
    def update(self, request, pk=None):
        cart_id = str(Cart.objects.get(user_id=str(request.user.id)).pk)
        if not CartItem.objects.filter(pk=pk).filter(cart_id=cart_id).exists(): 
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        cart_item_ins = CartItem.objects.get(pk=pk)
        edit_serializer = EditCartItemSerializer(cart_item_ins, data=request.data)
        if not edit_serializer.is_valid(): return Response(edit_serializer.errors, status.HTTP_400_BAD_REQUEST)
        edit_serializer.save()
        cart = getCart(request)
        return Response(cart, status=status.HTTP_202_ACCEPTED)

    @method_decorator(csrf_protect)
    def destroy(self, request, pk=None):
        cart_id = str(Cart.objects.get(user_id=str(request.user.id)).pk)
        if not CartItem.objects.filter(pk=pk).filter(cart_id=cart_id).exists(): 
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        cart_item_ins = CartItem.objects.get(pk=pk)
        cart_item_ins.delete()
        cart = getCart(request)
        return Response(cart, status=status.HTTP_202_ACCEPTED)
    

def getCart(request):
    cart_ins = Cart.objects.get(user_id=str(request.user.id))
    serialized_cart_data =  CartSerializer(cart_ins).data
    cart_items_ins = CartItem.objects.filter(pk__in=serialized_cart_data['items'])
    serialized_cart_data['items'] = CartItemSerializer(cart_items_ins, many=True).data
    product_pks =[ str(item['item']) for item in serialized_cart_data['items'] ]
    products = ProductListingPageView().getProducts(product_pks)
    serialized_cart_data['items'] = products
    return serialized_cart_data