from products.models import *
from products.serializers import *
from brands.models import Brand
from brands.serializers import BrandSerializer

def get_product_data(pks = (), many = False):
    Product_Instances = Product.objects.filter(pk__in=pks)
    product_data = ProductSerializer(Product_Instances, many=True).data
    
    brand_pks = tuple( str(data['brand']) for data in product_data )
    Brand_Instances = Brand.objects.filter(pk__in=brand_pks)
    brand_data = BrandSerializer(Brand_Instances, many=True).data

    product = list(zip(product_data, brand_data))
    print(product)

    return product_data if many else product_data[0]
    