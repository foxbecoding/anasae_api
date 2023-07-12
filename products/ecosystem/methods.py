from brands.models import Brand
from brands.serializers import BrandSerializer
from categories.models import Category, Subcategory
from categories.serializers import CategorySerializer, SubcategorySerializer
from products.models import *
from products.serializers import *

def filter_brand_data(obj):
    return {
        'pk': obj['pk'],
        'uid': obj['uid'],
        'name': obj['name'],
        'logo': obj['logo']
    }

def unzip_products(zip):
    product = zip[0]
    brand = zip[1]
    category = zip[2]

    product['brand'] = filter_brand_data(brand)
    product['category'] = category
    return product

def get_product_rel_data(product_data, key, model, serializer):
    pks = tuple( str(data[key]) for data in product_data )
    instances = model.objects.filter(pk__in=pks)
    return serializer(instances, many=True).data

def get_product_data(pks = (), many = False):
    Product_Instances = Product.objects.filter(pk__in=pks)
    product_data = ProductSerializer(Product_Instances, many=True).data
    brand_data = get_product_rel_data(product_data, 'brand', Brand, BrandSerializer)
    
    # category_pks = tuple( str(data['category']) for data in product_data )
    # Category_Instances = Category.objects.filter(pk__in=category_pks)
    # category_data = CategorySerializer(Category_Instances, many=True).data
    category_data = get_product_rel_data(product_data, 'category', Category, CategorySerializer)

    products_zip = list(zip(product_data, brand_data, category_data))
    products = [ unzip_products(zip) for zip in products_zip ]
    print(products)
    return product_data if many else product_data[0]
    