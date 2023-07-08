from django.db import models
from users.models import User

class Brand(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="brands", default='')
    uid = models.CharField(max_length=20, blank=False, unique=True)
    name = models.CharField(max_length=200, blank=False)
    bio = models.CharField(max_length=2000, blank=False)
    stripe_account_id = models.CharField(max_length=120, blank=True, unique=True, default='')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class BrandLogo(models.Model):
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE, related_name="logo")
    image = models.CharField(max_length=200, blank=False, default='')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class BrandOwner(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="owners")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_brands")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class BrandFollower(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_brands")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)