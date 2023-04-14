from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin, ModelAdmin
from django.utils.html import format_html

from AIShirts import settings
from .models import Item, Color, ItemWithColor, ShipmentStatus, Order, DeliveryType, DeliveryProvider, OrderItem, \
    Manufacturer, Size, ProductImage


@admin.register(ItemWithColor)
class ItemWithColorAdmin(admin.ModelAdmin):
    list_display = ('item', 'color', 'available_quantity', 'price', 'manufacturer')
    list_filter = ('item', 'color')
    search_fields = ('item__name', 'color__name')


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phone_number')
    search_fields = ('name', 'address', 'email', 'phone_number')


@admin.register(Size)
class ClothSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'chest_size', 'waist_size', 'hip_size', 'dress_length')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_name')
    list_filter = ('category',)
    search_fields = ('name', 'category')

    def category_name(self, obj):
        return [category.name for category in obj.category.all()]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')
    search_fields = ('name', 'hex_code')


@admin.register(ShipmentStatus)
class ShipmentStatusInline(admin.ModelAdmin):
    list_display = ('status', 'description')
    search_fields = ('status', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'shipped', 'shipping_address', 'order_date',
                    'shipping_method')
    list_filter = ('shipped', 'order_date')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    date_hierarchy = 'order_date'


@admin.register(DeliveryType)
class DeliveryTypeAdmin(ModelAdmin):
    list_display = ('name', 'price', 'delivery_provider')
    list_filter = ('delivery_provider',)
    search_fields = ('name', 'description')


@admin.register(DeliveryProvider)
class DeliveryProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'email', 'phone_number', 'logo_image')
    search_fields = ['name', 'website', 'email', 'phone_number']

    def logo_image(self, obj):
        if obj.logo_url:
            return '<img src="%s" width="50"/>' % obj.logo_url
        else:
            return '-'

    logo_image.allow_tags = True
    logo_image.short_description = 'Logo'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'prompt', 'order')


admin.site.register(OrderItem, OrderItemAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('product__name',)


admin.site.register(ProductImage, ProductImageAdmin)