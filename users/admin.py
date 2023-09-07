from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email'] # user_location
    search_fields = ['name', 'email']
    list_filter = ['is_active']

@admin.register(UserProducts)
class UserProductsAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'is_favourite', 'is_item_in_cart', 'quantity', 'view_count', 'updated_at']
    search_fields = ['user', 'product']
    list_filter = ['user',  'product']
    readonly_fields = ['user', 'product', 'is_favourite', 'is_item_in_cart', 'quantity', 'view_count', 'updated_at']

@admin.register(UserOrderHistory)
class UserOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'price', 'order_date']
    search_fields = ['user','product']
    list_filter = ['user', 'product']
    readonly_fields = ['user', 'product', 'quantity', 'price', 'order_date']

