import os
from enum import unique

from django.db import models
from keyring.backends import null

from aiintegration.models import Prompt, Image
from cust_and_stuff.models import Customer, DeliveryAddress

from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=20)
    chest_size = models.IntegerField(help_text='Chest size in cm')
    waist_size = models.IntegerField(help_text='Waist size in cm')
    hip_size = models.IntegerField(help_text='Hip size in cm')
    dress_length = models.IntegerField(help_text='Dress length in cm')

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class DeliveryProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    website = models.URLField(blank=True, help_text='URL of the delivery provider website')
    email = models.EmailField(blank=True, help_text='Contact email for the delivery provider')
    phone_number = models.CharField(max_length=20, blank=True,
                                    help_text='Contact phone number for the delivery provider')
    logo_url = models.URLField(blank=True, help_text='URL of the delivery provider logo')
    is_active = models.BooleanField(default=True, help_text='Indicates whether the delivery provider is active or not')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Date and time when the delivery provider was created')
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Date and time when the delivery provider was last updated')

    class Meta:
        verbose_name_plural = "Delivery Providers"

    def __str__(self):
        return self.name


class DeliveryType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    delivery_provider = models.ForeignKey(DeliveryProvider, on_delete=models.CASCADE, related_name='delivery_types')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Date and time when the category was created')
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Date and time when the category was last updated')

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('ItemWithColor', on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def delete(self, *args, **kwargs):
        if self.image_path:
            if os.path.isfile('media/'+self.image_path):
                os.remove('media/'+self.image_path)
        super(Image, self).delete(*args, **kwargs)



class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ItemWithColor(models.Model):
    item_code = models.IntegerField(null=True, default=0)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True)
    size = models.ManyToManyField(Size)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('item', 'color', 'item_code')

    def __str__(self):
        return f"{self.item.name} - {self.color.name}"


class ShipmentStatus(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Failed Delivery', 'Failed Delivery'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.status


class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    shipped = models.ForeignKey(ShipmentStatus, on_delete=models.SET_NULL, null=True, default=1)
    shipping_address = models.ForeignKey(DeliveryAddress, verbose_name="shipping_address", on_delete=models.SET_NULL,
                                         null=True)
    shipping_method = models.ForeignKey(DeliveryType, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"Order {self.pk} by {self.user.email}"


class OrderItem(models.Model):
    item = models.ForeignKey(ItemWithColor, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    prompt = models.ForeignKey(Prompt, verbose_name="prompt", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    gimage = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)


class Bucket(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name='bucket')
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    items = models.ManyToManyField(OrderItem)
