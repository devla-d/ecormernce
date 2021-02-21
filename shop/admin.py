from django.contrib import admin
from .models import Item,Order,Shipping,OrderItem
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",)}

admin.site.register(Order)
admin.site.register(Shipping)
admin.site.register(OrderItem)
admin.site.register(Item,ItemAdmin)



