from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin, ModelAdmin
from django.utils.html import format_html

from AIshirts import settings
from .models import Item, Color, ItemWithColor, ShipmentStatus, Order, DeliveryType, DeliveryProvider, OrderItem


@admin.register(ItemWithColor)
class ItemWithColorAdmin(admin.ModelAdmin):
    list_display = ('item', 'color', 'available_quantity')
    list_filter = ('item', 'color')
    search_fields = ('item__name', 'color__name')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_name', 'price', 'size', 'image_preview')
    list_filter = ('category', 'size')
    search_fields = ('name', 'category')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}{}" width="50"/>', settings.STATIC_URL, obj.image)
        else:
            return '-'

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
