from django.contrib import admin
from .models import Category, Product, Image, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id', 'user', 'address', 'phone',
                    'shipped', 'created']
    list_filter = ['shipped', 'created']
    inlines = [OrderItemInline]


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(OrderItem)
