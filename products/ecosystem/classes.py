from brands.models import Brand
from brands.serializers import *
from categories.models import Category, Subcategory
from categories.serializers import *
from products.models import *
from products.serializers import *
from pprint import pprint
from utils.helpers import filter_obj

class ProductData:
    def __init__(self, pks = [], many = False):
        self.pks, self.many, self.products = pks, many, None
        self.__get_product_data()
    
    def __get_product_data(self):
        if not Product.objects.filter(pk__in=self.pks).exists(): return []
        Product_Instances = Product.objects.filter(pk__in=self.pks)
        products_data = ProductSerializer(Product_Instances, many=True).data
        brand_data = self.__get_rel_data(products_data, 'brand', Brand, BrandProductPageSerializer)
        category_data = self.__get_rel_data(products_data, 'category', Category, CategoryProductPageSerializer)
        subcategory_data = self.__get_rel_data(products_data, 'subcategory', Subcategory, SubcategoryProductPageSerializer)
        
        for product in products_data:
            product['brand'] = self.__set_rel_data(product['brand'], brand_data)
            product['category'] = self.__set_rel_data(product['category'], category_data)
            product['subcategory'] = self.__set_rel_data(product['subcategory'], subcategory_data)

        self.products = products_data if self.many else products_data[0]

    def __get_rel_data(self, products, key, model, serializer):
        pks = []
        for product in products: 
            if str(product[key]) not in pks: pks.append(str(product[key]))
        instances = model.objects.filter(pk__in=pks)
        data = serializer(instances, many=True).data
        return data
    
    def __set_rel_data(self, value, rel_data):
        data = [ data for data in rel_data if str(value) == str(data['pk'])]
        return data if len(data) > 0 else None