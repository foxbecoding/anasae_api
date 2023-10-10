from brands.models import Brand
from brands.serializers import *
from categories.models import Category, Subcategory
from categories.serializers import *
from products.models import *
from products.serializers import *
from products.ecosystem.classes import ProductData
from utils.helpers import list_to_str
from pprint import pprint

class CategoryPageView:
    def __init__(self):
        pass

    def retrieveView(self, uid):
        instance = Category.objects.get(uid=uid)
        category_data = CategoryPageSerializer(instance).data
        product_listing_ins = ProductListing.objects.filter(pk__in=category_data['product_listings']) 
        category_data['product_listings'] = ProductListingSerializer(product_listing_ins, many=True).data
        base_variant_pks = [str(cat['base_variant']) for cat in category_data['product_listings']]
        base_variant_ins = ProductListingBaseVariant.objects.filter(pk__in=base_variant_pks)
        base_variant_data = ProductListingBaseVariantSerializer(base_variant_ins, many=True).data
        product_variant_pks = [str(v['product']) for v in base_variant_data]
        product_variants = ProductData(product_variant_pks, many=True).products
        listing_data = []
        for listing in category_data['product_listings']:
            base_variant = [pro for pro in product_variants if str(pro['listing_base_variant']) == str(listing['base_variant'])][0]
            
            base_variant_data = {
                'pk': base_variant['pk'],
                'uid': base_variant['uid'],
                'title': base_variant['title'],
                'price': base_variant['price']
            }
            
            listing = {
                'uid': listing['uid'],
                'title': listing['title'],
                'image': listing['image'],
                'base_variant': base_variant_data
            }
            listing_data.append(listing)
        category_data['product_listings'] = listing_data
            
        return category_data

class CategoryHomePageView:
    def __init__(self):
        pass

    def listView(self):
        instances = Category.objects.all()
        categories_data = CategoryHomePageSerializer(instances, many=True).data
        for cat in categories_data:
            product_listing_ins = ProductListing.objects.filter(pk__in=cat['product_listings'])[0:6] 
            cat['product_listings'] = ProductListingSerializer(product_listing_ins, many=True).data
            base_variant_pks = [str(cat['base_variant']) for cat in cat['product_listings']]
            base_variant_ins = ProductListingBaseVariant.objects.filter(pk__in=base_variant_pks)
            base_variant_data = ProductListingBaseVariantSerializer(base_variant_ins, many=True).data
            product_variant_pks = [str(v['product']) for v in base_variant_data]
            product_variants = ProductData(product_variant_pks, many=True).products
            listing_data = []
            for listing in cat['product_listings']:
                base_variant = [pro for pro in product_variants if str(pro['listing_base_variant']) == str(listing['base_variant'])][0]

                base_variant_data = {
                    'pk': base_variant['pk'],
                    'uid': base_variant['uid'],
                    'title': base_variant['title'],
                    'price': base_variant['price']
                }
                
                listing = {
                    'uid': listing['uid'],
                    'title': listing['title'],
                    'image': listing['image'],
                    'base_variant': base_variant_data
                }
                listing_data.append(listing)
            cat['product_listings'] = listing_data
        return categories_data