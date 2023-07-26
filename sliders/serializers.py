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
        model = Slider
        fields = [
            'pk',
            'name',
            'is_active'
        ]

class CreateSliderImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Slider
        fields = [ 'name' ]