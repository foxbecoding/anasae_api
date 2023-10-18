from django.contrib import admin
from cart.models import *
from utils.helpers import create_uid

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)