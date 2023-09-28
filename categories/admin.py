from django.contrib import admin
from categories.models import *
from utils.helpers import create_uid

# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryImage)
admin.site.register(CategoryProductSpecification)
admin.site.register(CategoryProductSpecificationItem)
admin.site.register(CategoryProductSpecificationItemOption)
admin.site.register(Subcategory)
admin.site.register(SubcategoryImage)
admin.site.register(SubcategoryProductSpecificationItem)
# print(create_uid('cat-'))  