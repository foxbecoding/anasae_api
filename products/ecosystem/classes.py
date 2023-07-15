from brands.models import Brand
from brands.serializers import *
from categories.models import Category, Subcategory
from categories.serializers import *
from products.models import *
from products.serializers import *
from utils.helpers import filter_obj

class ProductData:
    def __init__(self, pks = [], many = False):
        self.pks, self.many, self.products = pks, many, None
        self.__get_product_data()
    
    def __get_product_data(self):
        if not Product.objects.filter(pk__in=self.pks).exists(): return []
        Product_Instances = Product.objects.filter(pk__in=self.pks)
        products_data = ProductSerializer(Product_Instances, many=True).data
        brand = self.__get_product_rel_data(products_data, 'brand', Brand, BrandProductPageSerializer)
        category = self.__get_product_rel_data(products_data, 'category', Category, CategoryProductPageSerializer)
        subcategory = self.__get_product_rel_data(products_data, 'subcategory', Subcategory, SubcategoryProductPageSerializer)
        price = self.__get_product_rel_data(products_data, 'price', ProductPrice, ProductPagePriceSerializer)
        specifications = self.__get_product_rel_data(products_data, 'specifications', ProductSpecification, ProductSpecificationsSerializer)
        products_zip = tuple( zip(products_data, brand, category, subcategory, price, [specifications]) )
        products = tuple( self.__unzip_products(zip) for zip in products_zip )
        self.products = products if self.many else products[0]

    def __get_product_rel_data(self, product_data, key, model, serializer):
        pks = tuple( data[key] for data in product_data )
        if key == 'specifications': pks = pks[0]
        if not model.objects.filter(pk__in=pks).exists(): return [{}]
        instances = model.objects.filter(pk__in=pks)
        return serializer(instances, many=True).data

    def __unzip_products(self, zip):
        product, brand, category, subcategory, price, specifications = zip
        product_rel_data = (
            {'data': brand, 'key': 'brand'},
            {'data': price, 'key': 'price'},
            {'data': category, 'key': 'category'},
            {'data': subcategory, 'key': 'subcategory'},
            {'data': specifications, 'key': 'specifications'}
        )
        for data in product_rel_data: product[data['key']] = data['data']
        return product