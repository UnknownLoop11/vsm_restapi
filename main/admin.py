from django.contrib import admin

from main.models import Store, Customer, OrderDetails, File, Location
# Register your models here.

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'email', 'uid')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('reference_id', '__str__', 'store')

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass