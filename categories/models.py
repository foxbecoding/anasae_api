from django.db import models

class Category(models.Model):
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class CategoryImage(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="image")
    image = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    uid = models.CharField(max_length=20, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=2000, blank=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class SubcategoryImage(models.Model):
    subcategory = models.OneToOneField(Subcategory, on_delete=models.CASCADE, related_name="image")
    image = models.CharField(max_length=200, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class CategoryProductSpecification(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="product_specification")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class CategoryProductSpecificationItem(models.Model):
    category_product_specification = models.ForeignKey(CategoryProductSpecification, on_delete=models.CASCADE, related_name="items")
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class CategoryProductSpecificationItemOption(models.Model):
    category_product_specification_item = models.ForeignKey(CategoryProductSpecificationItem, on_delete=models.CASCADE, related_name="options")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class SubcategoryProductSpecification(models.Model):
    subcategory = models.OneToOneField(Subcategory, on_delete=models.CASCADE, related_name="product_specification")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class SubcategoryProductSpecificationItem(models.Model):
    subcategory_product_specification = models.ForeignKey(SubcategoryProductSpecification, on_delete=models.CASCADE, related_name="items")
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class SubcategoryProductSpecificationItemOption(models.Model):
    subcategory_product_specification_item = models.ForeignKey(SubcategoryProductSpecificationItem, on_delete=models.CASCADE, related_name="options")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)