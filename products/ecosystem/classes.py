from brands.models import Brand
from brands.serializers import *
from categories.models import Category, Subcategory
from categories.serializers import *
from products.models import *
from products.serializers import *
from pprint import pprint

class ProductData:
    def __init__(self, pks = [], many = False):
        self.pks, self.many, self.products = pks, many, None
        self.__get_product_data()
    
    def __get_product_data(self):
        if not Product.objects.filter(pk__in=self.pks).exists(): return []
        Product_Instances = Product.objects.filter(pk__in=self.pks)
        self.products = ProductSerializer(Product_Instances, many=True).data
        brand_data = self.__get_rel_data('brand', Brand, BrandProductPageSerializer)
        category_data = self.__get_rel_data('category', Category, CategoryProductPageSerializer)
        subcategory_data = self.__get_rel_data('subcategory', Subcategory, SubcategoryProductPageSerializer)
        price_data = self.__get_rel_data('price', ProductPrice, ProductPagePriceSerializer)
        spec_data = self.__get_rel_data('specifications', ProductSpecification, ProductSpecificationSerializer)
        images_data = self.__get_rel_data('images', ProductImage, ProductImageSerializer)

        for product in self.products:
            product['brand'] = self.__set_rel_data(product['brand'], brand_data)
            product['category'] = self.__set_rel_data(product['category'], category_data)
            product['subcategory'] = self.__set_rel_data(product['subcategory'], subcategory_data)
            product['price'] = self.__set_rel_data(product['price'], price_data)
        self.__set_rel_multi_data('specifications', spec_data)
        self.__set_rel_multi_data('images', images_data)

        if not self.many: self.products = self.products[0]

    def __get_rel_data(self, key, model, serializer):
        special_keys = ['images', 'specifications']
        if key not in special_keys:
            pks = list(map(lambda product: product[key], self.products))
            instances = model.objects.filter(pk__in=pks)
            return serializer(instances, many=True).data
        else:
            data = []
            pks_list = list(map(lambda product: product[key], self.products))
            for pkl in pks_list:
                instances = model.objects.filter(pk__in=pkl)
                data.append(serializer(instances, many=True).data)
            return data
        

    def __set_rel_data(self, value, rel_data):
        data = [ data for data in rel_data if str(value) == str(data['pk'])]
        return data[0] if len(data) > 0 else None
    
    def __set_rel_multi_data(self, key, rel_data):
        for x in zip(self.products, rel_data):
            product, data = x
            product[key] = data