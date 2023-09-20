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
            'isbn',
            'stripe_product_id',
            'quantity',
            'brand',
            'category',
            'subcategory',
            'price',
            'specifications',
            'images'
        ]

class EditProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'sku',
            'isbn',
            'quantity'
        ]

class BulkCreateProductSerializer(serializers.ListSerializer):
    def create(validated_data):
        group_id = create_uid('gid-')
        products_objs = []
        
        for data in validated_data: 
            products_objs.append(Product(
                uid = create_uid('pro-'),
                group_id = group_id,
                brand = data['brand'],
                category = data['category'],
                subcategory = data['subcategory'],
                title = data['title'],
                description = data['description'],
                quantity = data['quantity'],
                sku = data['sku'],
                isbn = data['isbn']
            ))
        
        instances = Product.objects.bulk_create(products_objs)
        
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
            'isbn',
            'quantity'
        ]