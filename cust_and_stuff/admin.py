from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, DeliveryAddress


class CustomerAdmin(UserAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'is_staff', 'generation_count', 'daily_limit', 'last_count',
        'delivery_address_full')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('generation_count',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Delivery address', {'fields': ('delivery_address',)}),
    )
    def delivery_address_full(self, obj):
        return obj.delivery_address.street_address + ','+ obj.delivery_address.city + ','+ obj.delivery_address.state + ','+ obj.delivery_address.zip_code

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'street_address', 'city', 'state', 'zip_code', 'country', 'phone_number')
    search_fields = ('street_address', 'city', 'state', 'zip_code', 'country', 'phone_number')

admin.site.register(Customer, CustomerAdmin)
