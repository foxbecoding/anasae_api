from rest_framework import serializers
from products.models import *
import os

env = os.getenv

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [
            'pk',
            'label',
            'value',
            'is_required',
            'product'
        ]

class EditProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['value']

class BulkEditProductSpecificationSerializer(serializers.ListSerializer):
    def __init__(self, instances, validated_data): 
        self._instances = instances
        self._validated_data = validated_data
        self.specifications = []
        self.__update()

    def __update(self):
        updated_instances = [ self.__set_instance_data(data) for data in zip(self._instances, self._validated_data) ]
        ProductSpecification.objects.bulk_update(updated_instances, fields=['value'])
        self.specifications = ProductSpecificationSerializer(updated_instances, many=True).data
        
    
    def __set_instance_data(self, data):
        instance, value = data
        instance.value = value['value']
        return instance 


class CreateProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [
            'label',
            'value',
            'is_required',
            'product'
        ]

class BulkCreateProductSpecificationSerializer(serializers.ListSerializer):
    def create(validated_data):
        instances = []
        for data in validated_data:
            instances.append(
                ProductSpecification(
                    product=data['product'], 
                    label=data['label'], 
                    value=data['value'],
                    is_required=data['is_required']
                )
            )
        instances = ProductSpecification.objects.bulk_create(instances)
        return ProductSpecificationSerializer(instances, many=True).data