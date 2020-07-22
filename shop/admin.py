from django.contrib import admin

# Register your models here.
from shop.models import *


admin.site.register(Item, admin.ModelAdmin)
admin.site.register(Order, admin.ModelAdmin)
admin.site.register(OrderItem, admin.ModelAdmin)
