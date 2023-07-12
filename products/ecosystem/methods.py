from brands.models import Brand
from brands.serializers import BrandSerializer
from categories.models import Category, Subcategory
from categories.serializers import CategorySerializer, SubcategorySerializer
from products.models import *
from products.serializers import *
from utils.helpers import filter_obj

def unzip_products(zip):
    product, brand, category, subcategory = zip
    product['brand'] = filter_obj(brand, filter = ['pk','uid','name','logo'])
    product['category'] = filter_obj(category, filter = ['pk','uid','title'])
    product['subcategory'] = filter_obj(subcategory, filter = ['pk','uid','title'])
    return product

def get_product_rel_data(product_data, key, model, serializer):
    pks = tuple( str(data[key]) for data in product_data )
    instances = model.objects.filter(pk__in=pks)
    return serializer(instances, many=True).data

def get_product_data(pks = (), many = False):
    Product_Instances = Product.objects.filter(pk__in=pks)
    product = ProductSerializer(Product_Instances, many=True).data
    brand = get_product_rel_data(product, 'brand', Brand, BrandSerializer)
    category = get_product_rel_data(product, 'category', Category, CategorySerializer)
    subcategory = get_product_rel_data(product, 'subcategory', Subcategory, SubcategorySerializer)
    products_zip = list(zip(product, brand, category, subcategory))
    products = tuple( unzip_products(zip) for zip in products_zip )
    return products if many else products[0]   