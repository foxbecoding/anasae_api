from brands.models import *
from brands.serializers import *

def get_brand_data(instance: Brand):
    brand_data = BrandSerializer(instance).data
    print(brand_data)