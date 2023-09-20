from rest_framework import serializers
from products.models import *
import stripe, os

env = os.getenv

class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = [
            'pk',
            'price',
            'stripe_price_id',
            'product'
        ]

class CreateProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = [
            'product',
            'price'
        ]

class BulkCreateProductPriceSerializer(serializers.ListSerializer):
    def create(validated_data):
        stripe_product_ids = [ data['product'].stripe_product_id for data in validated_data ]
        price_objs = []
        
        for data in validated_data: 
            price_objs.append(ProductPrice(
                product = data['product'],
                price = data['price']
            ))
        
        instances = ProductPrice.objects.bulk_create(price_objs)
        for data in zip(instances, stripe_product_ids):  
            instance, stripe_product_id = data     
            stripe_price = stripe.Price.create(
                unit_amount=instance.price,
                currency="usd",
                product=stripe_product_id,
            )

            instance.stripe_price_id = stripe_price.id
            instance.save()
        
        return ProductPriceSerializer(instances, many=True).data
    
class EditProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = [
            'price'
        ]
    
    def update(self, instance: ProductPrice, validated_data):
        Product_Instance = Product.objects.get(pk=instance.product_id)
        stripe_price = stripe.Price.create(
            unit_amount=int(validated_data['price']),
            currency="usd",
            product=str(Product_Instance.stripe_product_id),
        )
        instance.price = int(validated_data['price'])
        instance.stripe_price_id = stripe_price.id
        instance.save()
        return ProductPriceSerializer(instance).data

class ProductPagePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = [
            'pk',
            'price'
        ]