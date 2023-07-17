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

    # def validate(self, attrs):
        
        # Product_Instance.save()
        
        # if len(attrs.get('specifications')) > 0:
        #     spec_instances = []
        #     for spec in attrs.get('specifications'):
        #         spec_instances.append(self.pro_specs_ins(Product_Instance, spec))
        #     ProductSpecification.objects.bulk_create(spec_instances)

        # stripe_price = stripe.Price.create(
        #     unit_amount=attrs.get('price'),
        #     currency="usd",
        #     product=stripe_product.id,
        # )

        # Product_Price_Instance = ProductPrice.objects.create(
        #     product = Product_Instance,
        #     price=attrs.get('price'),
        #     stripe_price_id=stripe_price.id
        # )
        # Product_Price_Instance.save()

        # attrs['product_pk'] = Product_Instance.id
        # return attrs

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

class ProductSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [
            'pk',
            'label',
            'value',
            'is_required',
            'product'
        ]