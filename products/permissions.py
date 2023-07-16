from rest_framework.permissions import BasePermission
from products.models import *
from products.serializers import ProductSerializer
from brands.models import BrandOwner
from brands.serializers import BrandOwnerSerializer


class ProductPermission(BasePermission):
    message = "Access Denied!"   

    def has_object_permission(self, request, view, obj) -> bool:
        data = request.data
        Brand_Owner_Instances = BrandOwner.objects.filter(user_id=str(request.user.id))
        brand_owner_data = BrandOwnerSerializer(Brand_Owner_Instances, many=True).data
        if request.method == 'POST':
            brand_pks = [d['brand'] for d in data]
            for d in data:
                if 'brand' not in d: return False
            
            pks = [ str(brand['brand']) for brand in brand_owner_data ]
            for pk in brand_pks: 
                if str(pk) not in pks: return False
        
        if request.method == 'PUT':
            product_pk = obj['product_pk']
            if not Product.objects.filter(pk=product_pk).exists(): return False
            Product_Instance = Product.objects.get(pk=product_pk)
            product_data = ProductSerializer(Product_Instance).data
            brand_pk = str(product_data['brand'])
            brand_pks = [ str(brand['brand']) for brand in brand_owner_data ]
            if brand_pk not in brand_pks: return False

        return True