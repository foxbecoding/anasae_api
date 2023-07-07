from django.db import models
from users.models import User

class Brand(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="brand")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    name = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class BrandLogo(models.Model):
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE, related_name="logo")
    image = models.CharField(max_length=200, blank=False, default='')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)

class BrandOwner(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="owners")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="brand_owner")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
    deleted = models.DateTimeField(null=True)
