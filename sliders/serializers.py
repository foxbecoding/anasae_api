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
            'is_active'
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
    
    class Meta:
        model = SliderImage
        fields = [ 
            'slider',
            'image' 
        ]

    def validate(self, attrs):
        image = attrs.get('image')
        img = Image.open(image)
        valid_formats = ['PNG', 'JPEG']
        if img.format not in valid_formats:
            msg = 'Image must be in PNG or JPEG format'
            raise serializers.ValidationError({"image": msg}, code='authorization')
            
        return attrs
    
    def create(self, validated_data):
        print(validated_data)