from rest_framework import serializers
from products.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, requests, os, calendar, time

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
            'price'
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
    
    class Meta:
        model = Product
        fields = [
            'brand',
            'category',
            'subcategory' ,
            'title',
            'description',
            'sku',
            'isbn',
            'quantity',
            'price'
        ]

    def validate(self, attrs):
        group_id = None
        if 'group_id' in self.context['request'].data:
            group_id = self.context['request'].data['group_id']

        Product_Instance = Product.objects.create(
            uid = create_uid('pro-'),
            group_id = group_id,
            brand = attrs.get('brand'),
            category = attrs.get('category'),
            subcategory = attrs.get('subcategory'),
            title = attrs.get('title'),
            description = attrs.get('description'),
            quantity = attrs.get('quantity'),
            sku = attrs.get('sku') or None,
            isbn = attrs.get('isbn') or None
        )

        Product_Instance.save()
        stripe_product = stripe.Product.create(
            name=Product_Instance.title,
            metadata={ 'pk': Product_Instance.id }
        )

        Product_Instance.stripe_product_id = stripe_product.stripe_id
        Product_Instance.save()
        print(attrs.get('price'))
        # stripe.Price.create(
        #     unit_amount=1999,
        #     currency="usd",
        #     recurring={"interval": "month"},
        #     product="prod_O7khZ1x9KF5NEs",
        # )

        attrs['product_pk'] = Product_Instance.id
        return attrs