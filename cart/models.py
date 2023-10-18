from django.db import models
from users.models import User
from products.models import Product

class Cart(models.Model):
    uid = models.CharField(max_length=20, blank=False, unique=True, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item_in_carts")
    quantity = models.IntegerField(default=0, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)