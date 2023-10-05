from brands.models import Brand
from brands.serializers import *
from categories.models import Category, Subcategory
from categories.serializers import *
from products.models import *
from products.serializers import *
from utils.helpers import list_to_str
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

class ProductListingView:
    def __init__(self):
        pass

    def listView(self, user_id):
        brand_id = str(Brand.objects.get(creator=user_id).id)
        product_listing_ins = ProductListing.objects.filter(brand_id=brand_id)
        listings = ProductListingSerializer(product_listing_ins, many=True).data
        listings.sort(key=lambda x: x['pk'])
        cat_pks = [str(listing['category']) for listing in listings]
        category_ins = Category.objects.filter(pk__in = cat_pks)
        Categories = CategorySerializer(category_ins, many=True).data
        for listing in listings:
            products = ProductData(listing['products'], many=True).products
            active_prod = [prod for prod in products if prod['is_active']]
            inactive_prod = [prod for prod in products if not prod['is_active']]
            base_variant = [prod for prod in products if str(prod['listing_base_variant']) == str(listing['base_variant'])][0]
            listing['base_variant'] = base_variant
            listing['base_variant_text'] = list_to_str([spec['value'].upper() for spec in base_variant['specifications'] if spec['label'] == 'Color' or spec['label'] == 'Size'])
            listing['base_variant_images'] = [ img['image'] for img in base_variant['images'] ]
            listing_image = listing['image']
            if not listing_image and len(listing['base_variant_images']) > 0:
                listing_image = listing['base_variant_images'][0]
                listing_ins = ProductListing.objects.get(pk=listing['pk'])
                listing_ins.image = listing_image
                listing_ins.save()
            listing['image'] = listing_image
            listing['category'] = [cat for cat in Categories if str(cat['pk']) == str(listing['category'])][0]['title']
            listing['active_products_list'] = self.__set_listing_products_data(active_prod)
            listing['active_products'] = len(active_prod)
            listing['inactive_products'] = len(inactive_prod)
        return listings
    
    def retrieveView(self, uid):
        instance = ProductListing.objects.get(uid=uid)
        serialized_data = ProductListingSerializer(instance).data
        prod_ins = Product.objects.filter(pk__in=serialized_data['products'])
        prod_pks = [str(prod.id) for prod in prod_ins]
        products = ProductData(prod_pks, many=True).products
        products.sort(key=lambda x: x['pk'])
        active_products = [prod for prod in products if prod['is_active']]
        inactive_products = [prod for prod in products if not prod['is_active']]
        serialized_data['active_products'] = self.__set_listing_products_data(active_products)
        serialized_data['inactive_products'] = self.__set_listing_products_data(inactive_products)
        serialized_data['category'] = Category.objects.get(pk=serialized_data['category']).title
        return serialized_data

    def __set_listing_products_data(self, products):
        for prod in products:
            prod['price_int'] = prod['price']['price'] if prod['price'] else None
            prod['stock_status'] = 'in stock'
            if prod['quantity'] == 0:
                prod['stock_status'] = 'out of stock'
            if len(prod['specifications']) > 0:
                prod['color'] = [spec['value'] for spec in prod['specifications'] if spec['label'] == 'Color'][0].upper()
                prod['size'] = [spec['value'] for spec in prod['specifications'] if spec['label'] == 'Size'][0].upper()
                prod['variants'] = f"{prod['color']},{prod['size']}"
            else: 
                prod['color'] = ''
                prod['size']  = ''
        return products