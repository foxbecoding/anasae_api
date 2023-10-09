from rest_framework import serializers
from sliders.models import Slider, SliderImage
from utils.helpers import create_uid
from PIL import Image
import requests, os, calendar, time

env = os.getenv

class SliderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Slider
        fields = [
            'pk',
            'name',
            'is_active',
            'images'
        ]

class CreateSliderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Slider
        fields = [ 'name' ]

class SliderImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SliderImage
        fields = [
            'pk',
            'image',
            'is_active'
        ]

class CreateSliderImageSerializer(serializers.ModelSerializer):
    upload = serializers.ImageField(write_only=True)
    class Meta:
        model = SliderImage
        fields = [ 
            'slider',
            'upload' 
        ]

    def validate(self, attrs):
        image = attrs.get('upload')
        img = Image.open(image)
        valid_formats = ['PNG','JPEG','JPG','AVIF']
        if img.format not in valid_formats:
            msg = 'Image must be in .png, .avif, or .jpg format'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        return attrs
    
    def create(self, validated_data):
        image = self.__get_image(validated_data['upload'])
        slider_instance = Slider.objects.get(pk=str(validated_data['slider']))
        instance = SliderImage.objects.create(
            slider = slider_instance,
            image = image
        )
        instance.save()
        return SliderImageSerializer(instance).data

    def __get_image(self, image):
        img = Image.open(image)
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        image_name = create_uid('slide-')+f'-{time_stamp}.{img.format.lower()}'
        image_path = str(env('CDN_SLIDER_DIR')+image_name)
    
        upload = requests.post(
            f'{env("CDN_HOST_API")}{env("CDN_UPLOAD_IMAGE")}',
            data = {
                "file_path": env('CDN_SLIDER_DIR'),
                "image_name": image_name
            },
            files={ "image": image.file.getvalue() }
        )

        if upload.status_code != 200:
            msg = 'Please try again'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        return image_path
