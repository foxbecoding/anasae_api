from django.db import models
from users.models import User
from categories.models import Category, Subcategory
from brands.models import Brand

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, related_name="products", blank=True, null=True)
    uid = models.CharField(max_length=20, blank=False, unique=True)
    stripe_product_id = models.CharField(max_length=50, blank=False, unique=True, default="")
    sku = models.CharField(max_length=50, blank=True, unique=True)
    isbn = models.CharField(max_length=14, blank=True, null=True, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=10000, blank=False)
    quantity = models.IntegerField(blank=False, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductPrice(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="price")
    price = models.IntegerField(default=0, blank=False)
    stripe_price_id = models.CharField(max_length=50, blank=False, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductSpecification(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="specifications")
    label = models.CharField(max_length=100, blank=False)
    value = models.CharField(max_length=100, blank=True, null=True, default='')
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    title = models.CharField(max_length=250, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductVariantItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=10000, blank=False)
    stripe_product_id = models.CharField(max_length=50, blank=False, unique=True, default="")
    sku = models.CharField(max_length=50, blank=True, unique=True)
    quantity = models.IntegerField(default=0, blank=False)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductVariantItemPrice(models.Model):
    product_variant_item = models.OneToOneField(ProductVariantItem, on_delete=models.CASCADE, related_name="price")
    price = models.IntegerField(default=0, blank=False)
    stripe_price_id = models.CharField(max_length=50, blank=False, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductVariantItemSpecification(models.Model):
    product_variant_item = models.ForeignKey(ProductVariantItem, on_delete=models.CASCADE, related_name="specifications")
    label = models.CharField(max_length=100, blank=False)
    value = models.CharField(max_length=100, blank=True, null=True, default='')
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductVariantItemImage(models.Model):
    product_variant_item = models.ForeignKey(ProductVariantItem, on_delete=models.CASCADE, related_name="images")
    image = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_reviews")
    comment = models.CharField(max_length=500, blank=False)
    stars = models.IntegerField(default=0, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductWishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wish_list")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductWishListItem(models.Model):
    wish_list = models.ForeignKey(ProductWishList, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wish_list_items")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)