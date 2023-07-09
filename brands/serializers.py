from rest_framework import serializers
from brands.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, requests, os, calendar, time

env = os.getenv

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'pk',
            'uid',
            'name',
            'bio',
            'stripe_account_id',
            'owners',
            'followers',
            'logo'
        ]

class EditBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = [
            'name',
            'bio',
        ]

class CreateBrandSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Brand
        fields = [
            'name',
            'bio',
        ]

    def validate(self, attrs):
        request = self.context['request']

        Stripe_Account = stripe.Account.create(
            type="custom",
            country="US",
            email=request.user.email,
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            }
        )

        Brand_Instance = Brand.objects.create(
            creator = request.user,
            uid = create_uid('b-'),
            stripe_account_id = Stripe_Account.id,
            name = attrs.get('name'),
            bio = attrs.get('bio')
        )
        Brand_Instance.save()

        Brand_Owner_Instance = BrandOwner.objects.create(
            brand = Brand_Instance,
            owner = request.user
        )
        Brand_Owner_Instance.save()

        stripe.Account.modify(
            Stripe_Account.id,
            metadata={ "brand_id": Brand_Instance.id },
        )
        
        attrs['brand'] = Brand_Instance
        return attrs
    
class BrandOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandOwner
        fields = [
            'pk',
            'brand',
            'owner'
        ]

class CreateBrandOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandOwner
        fields = [
            'brand',
            'owner'
        ]
    
    def validate(self, attrs):
        brand = attrs.get('brand')
        owner = attrs.get('owner')

        if BrandOwner.objects.filter(brand_id=brand.id).filter(owner_id=owner.id).exists():
            msg = 'User is already an owner.'
            raise serializers.ValidationError({"error": msg}, code='authorization')
        
        Brand_Owner_Instance = BrandOwner.objects.create(
            brand = brand,
            owner = owner
        )

        Brand_Owner_Instance.save()

        attrs['brand_owner'] = Brand_Owner_Instance
        return attrs

class BrandLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandLogo
        fields = [
            'pk',
            'image'
        ]

class CreateBrandLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandLogo
        fields = [
            'brand'
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
        image_name = create_uid('bl-')+f'-{time_stamp}.{img.format.lower()}'
        image_path = str(env('CDN_BRAND_LOGO_DIR')+image_name)
    
        upload = requests.post(
            f'{env("CDN_HOST_API")}{env("CDN_UPLOAD_IMAGE")}',
            data = {
                "file_path": env('CDN_BRAND_LOGO_DIR'),
                "image_name": image_name
            },
            files={ "image": image.file.getvalue() }
        )

        if upload.status_code != 200:
            msg = 'Please try again'
            raise serializers.ValidationError({"image": msg}, code='authorization')

        Brand_Logo_Instance = BrandLogo.objects.create(
            brand = attrs.get('brand'),
            image = image_path
        )

        Brand_Logo_Instance.save()
        attrs['brand_logo'] = Brand_Logo_Instance
        attrs['brand'] = attrs.get('brand')
        return attrs
    
class BrandFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandFollower
        fields = [
            'pk',
            'brand',
            'user'
        ]

class CreateBrandFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandFollower
        fields = [
            'brand'
        ]
    
    def validate(self, attrs):
        brand = attrs.get('brand')
        user = self.context['request'].user

        if BrandFollower.objects.filter(brand_id=brand.id).filter(user_id=user.id).exists():
            msg = 'User is already following this brand.'
            raise serializers.ValidationError({"error": msg}, code='authorization')
        
        Brand_Follower_Instance = BrandFollower.objects.create(
            brand = brand,
            user = user
        )

        Brand_Follower_Instance.save()

        attrs['brand_follower'] = Brand_Follower_Instance
        return attrs