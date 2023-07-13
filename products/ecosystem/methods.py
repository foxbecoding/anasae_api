from brands.models import Brand
from brands.serializers import BrandSerializer
from categories.models import Category, Subcategory
from categories.serializers import CategorySerializer, SubcategorySerializer
from products.models import *
from products.serializers import *
from utils.helpers import filter_obj

def unzip_products(zip):
    product, brand, category, subcategory, price = zip
    product_rel_data = (
        {'data': brand, 'key': 'brand', 'filter': ['pk','uid','name','logo']},
        {'data': price, 'key': 'price', 'filter': ['price']},
        {'data': category, 'key': 'category', 'filter': ['pk','uid','title']},
        {'data': subcategory, 'key': 'subcategory', 'filter': ['pk','uid','title']}
    )
    for data in product_rel_data: product[data['key']] = filter_obj(data['data'], data['filter'])
    return product

def get_product_rel_data(product_data, key, model, serializer):
    pks = tuple( str(data[key]) for data in product_data )
    instances = model.objects.filter(pk__in=pks)
    return serializer(instances, many=True).data

def get_product_data(pks = [], many = False):
    if not Product.objects.filter(pk__in=pks).exists(): return []
    Product_Instances = Product.objects.filter(pk__in=pks)
    product = ProductSerializer(Product_Instances, many=True).data
    brand = get_product_rel_data(product, 'brand', Brand, BrandSerializer)
    category = get_product_rel_data(product, 'category', Category, CategorySerializer)
    subcategory = get_product_rel_data(product, 'subcategory', Subcategory, SubcategorySerializer)
    price = get_product_rel_data(product, 'price', ProductPrice, ProductPriceSerializer)
    products_zip = tuple( zip(product, brand, category, subcategory, price) )
    products = tuple( unzip_products(zip) for zip in products_zip )
    return products if many else products[0]   