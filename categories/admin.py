from django.contrib import admin
from categories.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryImage)
admin.site.register(CategoryProductSpecification)
admin.site.register(CategoryProductSpecificationItem)
admin.site.register(Subcategory)
admin.site.register(SubcategoryImage)
admin.site.register(SubcategoryProductSpecificationItem)