from django.contrib import admin
from .models import Customer, DeliveryAddress


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'is_staff', 'generation_count', 'daily_limit', 'last_count', 'phone_number'
        )
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('generation_count',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Delivery address', {'fields': ('delivery_address',)}),
    )

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'street_address', 'city', 'state', 'zip_code', 'country')
    search_fields = ('street_address', 'city', 'state', 'zip_code', 'country')

admin.site.register(Customer, CustomerAdmin)
