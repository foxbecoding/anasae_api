from rest_framework import serializers
from products.models import *
from utils.helpers import create_uid
from PIL import Image
import requests, os, calendar, time

env = os.getenv

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
            valid_formats = ['PNG','JPEG','JPG','AVIF']
            if img.format not in valid_formats:
                msg = 'Image must be in .png, .avif, or .jpg format'
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
  