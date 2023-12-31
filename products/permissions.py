from rest_framework.permissions import BasePermission
from products.models import *
from products.serializers import *
from brands.models import BrandOwner
from brands.serializers import BrandOwnerSerializer, BrandSerializer
from utils.helpers import key_exists
import re
from pprint import pprint


class ProductPermission(BasePermission):
    message = "Access Denied!"   

    def has_object_permission(self, request, view, obj) -> bool:
        data = request.data
        Brand_Owner_Instances = BrandOwner.objects.filter(user_id=str(request.user.id))
        brand_owner_data = BrandOwnerSerializer(Brand_Owner_Instances, many=True).data

        if request.method == 'GET' and 'action' in obj:
            if not key_exists('pks', obj): return False
            if obj['action'] != 'list': return False
            for pk in obj['pks']:
                if not bool(re.match('^[0-9]+$', pk)): return False             

        if request.method == 'POST':
            brand_pks = [d['brand'] for d in data]
            for d in data:
                if not key_exists('brand', d): return False
            
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

class ProductPricePermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        if not key_exists('product', request.data): return False
        if request.method == 'POST':
            product_pks = [str(data['product']) for data in request.data]
            if not is_brand_product(request, product_pks): return False
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        Brand_Owner_Instances = BrandOwner.objects.filter(user_id=str(request.user.id))
        brand_owner_data = BrandOwnerSerializer(Brand_Owner_Instances, many=True).data
        
        data = request.data
        if not key_exists('product', data): return False
        product_price_pk = obj['product_price_pk']
        product_pk = data['product']
        
        if not ProductPrice.objects.filter(pk=product_price_pk).exists(): return False
        if not Product.objects.filter(pk=product_pk).exists(): return False
        Product_Instance = Product.objects.get(pk=product_pk)
        product_data = ProductSerializer(Product_Instance).data
        
        brand_pk = str(product_data['brand'])
        brand_pks = [ str(brand['brand']) for brand in brand_owner_data ]
        if brand_pk not in brand_pks: return False
        
        return True
    
class ProductSpecificationPermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        if request.method == 'POST':
            if not key_exists('product', request.data): return False
            product_pks = list(dict.fromkeys([str(data['product']) for data in request.data]))
            if not is_brand_product(request, product_pks): return False
        return True
    
    def has_object_permission(self, request, view, obj):
        pks = obj['pks']
        if len(pks) == 0: return False
        for pk in pks:
            if not ProductSpecification.objects.filter(pk=pk).exists(): return False
        
        Prod_Spec_Instances = ProductSpecification.objects.filter(pk__in=pks)
        product_pks = list(dict.fromkeys([ str(instance.product_id) for instance in Prod_Spec_Instances ])) 
        
        if not is_brand_product(request, product_pks): return False
        return True
    
class ProductImagePermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        if request.method == 'POST':
            if not key_exists('product', request.data): return False
            if not is_brand_product(request, [request.data['product']]): return False
        return True
    
    def has_object_permission(self, request, view, obj):
        image_pks = obj['image_pks']
        for pk in image_pks:
            if not ProductImage.objects.filter(pk=pk).exists(): return False
        instances = ProductImage.objects.filter(pk__in=image_pks)
        product_pks = [ ins.product_id for ins in instances ]
        if not is_brand_product(request, product_pks): return False
        return True
        

class ProductDimensionPermission(BasePermission):
    message = "Access Denied!"   
    
    def has_object_permission(self, request, view, obj):
        instance=obj['instance']
        data = ProductDimensionSerializer(instance).data
        if not is_brand_product(request, [data['product']]): return False
        return True
        

class ProductListingPermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        user_id = str(request.user.id)
        if not Brand.objects.filter(creator=user_id).exists(): return False
        return True

    def has_object_permission(self, request, view, obj):
        uid = obj['uid']
        user_id = str(request.user.id)
        brand_id = str(Brand.objects.get(creator=user_id).id)
        if not ProductListing.objects.filter(uid=uid).filter(brand_id=brand_id).exists(): return False
        return True

class ProductListingBaseVariantPermission(BasePermission):
    message = "Access Denied!"   

    def has_permission(self, request, view):
        user_id = str(request.user.id)
        if not Brand.objects.filter(creator=user_id).exists(): return False
        return True
    
    def has_object_permission(self, request, view, obj):
        base_variant_pk = obj['pk']
        product_pk = request.data['product']
        user_id = str(request.user.id)
        brand_id = Brand.objects.get(creator=user_id).id

        if 'product' not in request.data: return False
        if not Product.objects.filter(pk=product_pk).filter(brand_id=brand_id).exists(): return False

        product_data = ProductSerializer(Product.objects.get(pk=product_pk)).data
        if not ProductListing.objects.filter(pk=product_data['listing']).filter(brand_id=brand_id).exists(): return False
        # if str(product_data['listing_base_variant']) != str(base_variant_pk): return False

        return True

def is_brand_product(request, product_pks):
    Brand_Owner_Instances = BrandOwner.objects.filter(user_id=str(request.user.id))
    brand_owner_data = BrandOwnerSerializer(Brand_Owner_Instances, many=True).data
    for product_pk in product_pks:
        if not Product.objects.filter(pk=product_pk).exists(): return False
        Product_Instance = Product.objects.get(pk=product_pk)
        product_data = ProductSerializer(Product_Instance).data
        brand_pk = str(product_data['brand'])
        brand_pks = [ str(brand['brand']) for brand in brand_owner_data ]
        if brand_pk not in brand_pks: return False
    return True