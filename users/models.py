from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    uid = models.CharField(max_length=20, blank=True, unique=True)
    agreed_to_toa = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True)
    display_name = models.CharField(max_length=150, blank=True, null=True, default='')
    first_name = models.CharField(max_length=300, blank=False)
    last_name = models.CharField(max_length=300, blank=False)
    stripe_customer_id = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="image")
    image = models.CharField(max_length=200, blank=False, null=False, default='')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class UserGender(models.Model):
    gender = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class UserGenderChoice(models.Model):
    user_gender = models.ForeignKey(UserGender, on_delete=models.CASCADE, related_name="choices", default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gender_choice", default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=200, blank=False)
    phone_number = models.CharField(max_length=100, blank=False)
    street_address = models.CharField(max_length=1000, blank=False)
    street_address_ext = models.CharField(max_length=1000, blank=True)
    country = models.CharField(max_length=200, blank=False, default='')
    state = models.CharField(max_length=200, blank=False, default='')
    city = models.CharField(max_length=200, blank=False)
    postal_code = models.CharField(max_length=200, blank=False, default='')
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class UserLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logins")
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country_code = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    device = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)