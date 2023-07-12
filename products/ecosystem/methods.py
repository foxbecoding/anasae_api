from products.models import *
from products.serializers import *
from brands.models import Brand
from brands.serializers import BrandSerializer

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

    product['brand'] = filter_brand_data(brand)

    return product

def get_product_data(pks = (), many = False):
    Product_Instances = Product.objects.filter(pk__in=pks)
    product_data = ProductSerializer(Product_Instances, many=True).data
    
    brand_pks = tuple( str(data['brand']) for data in product_data )
    Brand_Instances = Brand.objects.filter(pk__in=brand_pks)
    brand_data = BrandSerializer(Brand_Instances, many=True).data

    products_zip = list(zip(product_data, brand_data))
    products_unzip = [ unzip_products(zip) for zip in products_zip ]

    return product_data if many else product_data[0]
    