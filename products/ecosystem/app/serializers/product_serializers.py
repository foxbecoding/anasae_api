from rest_framework import serializers
from products.models import *
from utils.helpers import create_uid
import stripe, os

env = os.getenv

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'pk',
            'uid',
            'title',
            'description',
            'sku',
            'stripe_product_id',
            'quantity',
            'is_active',
            'brand',
            'listing',
            'category',
            'subcategory',
            'price',
            'dimension',
            'specifications',
            'images',
            'created',
            'updated'
        ]

class EditProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'sku',
            'quantity',
            'is_active'
        ]

class BulkCreateProductSerializer(serializers.ListSerializer):
    def create(validated_data):
        products_objs = []
        
        product_listing_ins = ProductListing.objects.create(
            brand=validated_data[0]['brand'],
            category = validated_data[0]['category'],
            title=validated_data[0]['title'],
            uid=create_uid('lid-')
        )
        
        product_listing_ins.save()

        for data in validated_data: 
            products_objs.append(Product(
                uid = create_uid('pro-'),
                listing = product_listing_ins,
                brand = data['brand'],
                category = data['category'],
                subcategory = data['subcategory'],
                title = data['title'],
                description = data['description'],
                quantity = data['quantity'],
                sku = data['sku'],
                is_active = data['is_active']
            ))
        
        instances = Product.objects.bulk_create(products_objs)
        
        ProductListingBaseVariant.objects.create(
            product = instances[0],
            product_listing = product_listing_ins
        ).save()

        for ins in instances:        
            stripe_product = stripe.Product.create(
                name=ins.title,
                metadata={ 'pk': ins.id }
            )

            ins.stripe_product_id = stripe_product.id
            ins.save()
    
        return [str(ins.id) for ins in instances]
    
class CreateProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'brand',
            'title',
            'category',
            'subcategory',
            'description',
            'sku',
            'quantity',
            'is_active'
        ]