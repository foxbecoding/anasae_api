from django.contrib import admin
from products.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductPrice)
admin.site.register(ProductSpecification)
admin.site.register(ProductListing)
admin.site.register(ProductListingBaseVariant)
