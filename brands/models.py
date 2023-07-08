from django.db import models
from users.models import User

class Brand(models.Model):
    owners = models.ManyToManyField(User, related_name="brands")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    name = models.CharField(max_length=200, blank=False)
    bio = models.CharField(max_length=2000, blank=False)
    stripe_account_id = models.CharField(max_length=120, blank=True, unique=True, default='')
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