from brands.models import Brand
from brands.serializers import BrandSerializer
from categories.models import Category, Subcategory
from categories.serializers import CategorySerializer, SubcategorySerializer
from products.models import *
from products.serializers import *

def filter_data(obj, filter = []):
    if len(filter) == 0 or len(obj) == 0: return obj
    newDict = dict()
    for (key, value) in obj.items():
        if key in filter:
            newDict[key] = value
    return newDict

def unzip_products(zip):
    product = zip[0]
    brand = zip[1]
    category = zip[2]
    subcategory = zip[3]

    product['brand'] = filter_data(brand, filter = ['pk','uid','name','logo'])
    product['category'] = filter_data(category, filter = ['pk','uid','title'])
    product['subcategory'] = filter_data(subcategory, filter = ['pk','uid','title'])
    return product

def get_product_rel_data(product_data, key, model, serializer):
    pks = tuple( str(data[key]) for data in product_data )
    instances = model.objects.filter(pk__in=pks)
    return serializer(instances, many=True).data

def get_product_data(pks = (), many = False):
    Product_Instances = Product.objects.filter(pk__in=pks)
    product_data = ProductSerializer(Product_Instances, many=True).data
    brand_data = get_product_rel_data(product_data, 'brand', Brand, BrandSerializer)
    category_data = get_product_rel_data(product_data, 'category', Category, CategorySerializer)
    subcategory_data = get_product_rel_data(product_data, 'subcategory', Subcategory, SubcategorySerializer)
    products_zip = list(zip(product_data, brand_data, category_data, subcategory_data))
    products = [ unzip_products(zip) for zip in products_zip ]
    return products if many else products[0]   