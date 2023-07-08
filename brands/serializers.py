from rest_framework import serializers
from brands.models import *
from utils.helpers import create_uid
from PIL import Image
import stripe, requests, os, calendar, time

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