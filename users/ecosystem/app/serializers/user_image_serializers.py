from rest_framework import serializers
from users.models import *
from utils.helpers import create_uid
from PIL import Image
import requests, os, calendar, time


env = os.getenv

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = [
            'pk',
            'image'
        ]

class CreateUserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = [
            'user'
        ]

    def validate(self, attrs):
        request_data = self.context['request'].data

        if 'image' not in request_data:
            msg = 'Please upload an image'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        if not request_data['image']:
            msg = 'Please upload an image'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        image = request_data['image']
        
        img = Image.open(image)
        valid_formats = ['PNG', 'JPEG']
        if img.format not in valid_formats:
            msg = 'Image must be in PNG or JPEG format'
            raise serializers.ValidationError({"image": msg}, code='authorization')
        
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        image_name = create_uid('ui-')+f'-{time_stamp}.{img.format.lower()}'
        image_path = str(env('CDN_USER_IMAGE_DIR')+image_name)
    
        upload = requests.post(
            f'{env("CDN_HOST_API")}{env("CDN_UPLOAD_IMAGE")}',
            data = {
                "file_path": env('CDN_USER_IMAGE_DIR'),
                "image_name": image_name
            },
            files={ "image": image.file.getvalue() }
        )

        if upload.status_code != 200:
            msg = 'Please try again'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        User_Image_Instance = UserImage.objects.create(
            user = attrs.get('user'),
            image = image_path
        )

        User_Image_Instance.save()
        attrs['user_image'] = User_Image_Instance
        return attrs