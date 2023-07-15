from rest_framework import serializers
from products.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, requests, os, calendar, time, json

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
            'specifications'
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

class CreateProductSerializer(serializers.ModelSerializer):
    
    price = serializers.IntegerField(write_only=True)
    specifications = serializers.ListField(write_only=True)
    
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
            'quantity',
            'price',
            'specifications'
        ]

    def validate(self, attrs):
        request_data = self.context['request'].data
        
        group_id = None
        if 'group_id' in request_data:
            group_id = self.context['request'].data['group_id']

        Product_Instance = Product.objects.create(
            uid = create_uid('pro-'),
            group_id = group_id,
            brand = attrs.get('brand'),
            category = attrs.get('category'),
            title = attrs.get('title'),
            description = attrs.get('description'),
            quantity = attrs.get('quantity'),
            sku = attrs.get('sku') or None,
            isbn = attrs.get('isbn') or None
        )

        if attrs.get('subcategory'):  Product_Instance.subcategory = attrs.get('subcategory')

        Product_Instance.save()
        stripe_product = stripe.Product.create(
            name=Product_Instance.title,
            metadata={ 'pk': Product_Instance.id }
        )

        Product_Instance.stripe_product_id = stripe_product.id
        Product_Instance.save()
        
        if len(attrs.get('specifications')) > 0:
            spec_instances = []
            for spec in attrs.get('specifications'):
                spec_instances.append(self.pro_specs_ins(Product_Instance, spec))
            ProductSpecification.objects.bulk_create(spec_instances)

        stripe_price = stripe.Price.create(
            unit_amount=attrs.get('price'),
            currency="usd",
            product=stripe_product.id,
        )

        Product_Price_Instance = ProductPrice.objects.create(
            product = Product_Instance,
            price=attrs.get('price'),
            stripe_price_id=stripe_price.id
        )
        Product_Price_Instance.save()

        attrs['product_pk'] = Product_Instance.id
        return attrs

    def pro_specs_ins(self, product, spec):
        Product_Specification_Instance = ProductSpecification(
            product=product, 
            label=spec['label'], 
            value=spec['value'],
            is_required=spec['is_required']
        )
        return Product_Specification_Instance
    
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = [
            'pk',
            'price',
            'stripe_price_id'
        ]