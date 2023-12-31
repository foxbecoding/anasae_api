from django.db import models
from users.models import User
from categories.models import Category, Subcategory
from brands.models import Brand

class ProductListing(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="product_listings")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="product_listings", null=True)
    title = models.CharField(max_length=90, blank=False, default='')
    uid = models.CharField(max_length=20, blank=False, unique=True)
    image = models.CharField(max_length=200, blank=False, default='')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name="products", default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, related_name="products", blank=True, null=True)
    uid = models.CharField(max_length=20, blank=False, unique=True)
    stripe_product_id = models.CharField(max_length=50, blank=False, null=False, default="")
    sku = models.CharField(max_length=50, blank=True, null=True, unique=True)
    title = models.CharField(max_length=90, blank=False)
    description = models.TextField(max_length=300, blank=False)
    quantity = models.IntegerField(default=0, blank=False, null=False)
    variant_order = models.IntegerField(default=1, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductListingBaseVariant(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="listing_base_variant")
    product_listing = models.OneToOneField(ProductListing, on_delete=models.CASCADE, related_name="base_variant")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductDimension(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="dimension")
    length = models.CharField(max_length=20, blank=False, null=False, default="")
    width = models.CharField(max_length=20, blank=False, null=False, default="")
    height = models.CharField(max_length=20, blank=False, null=False, default="")
    weight = models.CharField(max_length=20, blank=False, null=False, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductPrice(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="price")
    price = models.IntegerField(default=0, blank=False)
    stripe_price_id = models.CharField(max_length=50, blank=True, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    label = models.CharField(max_length=30, blank=False)
    value = models.CharField(max_length=30, blank=True, null=True, default='')
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(default=True, blank=False)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wish_list", default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wish_list_items", default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class ProductConfig(models.Model):
    image_limit = models.IntegerField(default=7)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)