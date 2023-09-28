from rest_framework import serializers
from products.models import ProductDimension
import stripe, os

env = os.getenv

class ProductDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDimension
        fields = [
            'pk',
            'length',
            'width',
            'height',
            'weight',
            'product'
        ]

class CreateProductDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDimension
        fields = [
            'length',
            'width',
            'height',
            'weight',
            'product'
        ]

class BulkCreateProductDimensionSerializer(serializers.ListSerializer):
    def create(validated_data):
        objs = []
        
        for data in validated_data: 
            objs.append(ProductDimension(
                product = data['product'],
                length = data['length'],
                width = data['width'],
                height = data['height'],
                weight = data['weight']
            ))
        
        instances = ProductDimension.objects.bulk_create(objs)
        
        return ProductDimensionSerializer(instances, many=True).data
    
class EditProductDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDimension
        fields = [
            'length',
            'width',
            'height',
            'weight',
        ]

