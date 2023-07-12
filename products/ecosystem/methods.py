from products.models import *
from products.serializers import *

def get_product_data(pks = (), many = False):
    # Product_Instances = Product.objects.fitler(pk__in=pks)
    # product_data = ProductSerializer(Product_Instances, many=True).data
    print(pks)
    # return product_data if many else product_data[0]