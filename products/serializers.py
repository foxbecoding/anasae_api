from rest_framework import serializers
from products.models import *
from utils.helpers import create_uid, str_to_list
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
    
class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = [
            'product',
            'image',
            'pk'
        ]

class CreateProductImageSerializer(serializers.ModelSerializer):
    images = serializers.ListField(write_only=True)
    class Meta:
        model = ProductImage
        fields = [
            'product',
            'images'
        ]

    def validate(self, attrs):
        images = attrs.get('images')
        for image in images:
            img = Image.open(image)
            valid_formats = ['PNG', 'JPEG']
            if img.format not in valid_formats:
                msg = 'Image must be in PNG or JPEG format'
                raise serializers.ValidationError({"image": msg}, code='authorization')
            
        return attrs

class BulkCreateProductImageSerializer(serializers.ListSerializer):
    def __init__(self, validated_data): 
        self.image_data = validated_data
        self.product_images = None
        self.__create()

    def __create(self):
        product = self.image_data['product']
        images = self.image_data['images']
        image_paths = self.__upload(images)
        product_image_objs = self.__image_instances(image_paths, product)
        instances = ProductImage.objects.bulk_create(product_image_objs)
        self.product_images = ProductImageSerializer(instances, many=True).data
        

    def __image_instances(self, image_paths, product):
        instances = []
        for image in image_paths:
            instances.append(ProductImage(
                image=image,
                product=product
            ))
        return instances

    def __upload(self, images):
        image_paths = []
        for image in images:
            img = Image.open(image)
            current_GMT = time.gmtime()
            time_stamp = calendar.timegm(current_GMT)
            image_name = create_uid('pi-')+f'-{time_stamp}.{img.format.lower()}'
            image_path = str(env('CDN_PRODUCT_IMAGE_DIR')+image_name)
            image_paths.append(image_path)
            upload = requests.post(
                f'{env("CDN_HOST_API")}{env("CDN_UPLOAD_IMAGE")}',
                data = {
                    "file_path": env('CDN_PRODUCT_IMAGE_DIR'),
                    "image_name": image_name
                },
                files={ "image": image.file.getvalue() }
            )

            if upload.status_code != 200:
                msg = 'Please try again'
                raise serializers.ValidationError({"image": msg}, code='authorization')
            
        return image_paths
  