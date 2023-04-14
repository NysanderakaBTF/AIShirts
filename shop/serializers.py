from itertools import product

from rest_framework import serializers

from aiintegration.models import Image, Prompt
from aiintegration.serializers import ImageSerializer, PromptSerializer
from cust_and_stuff.models import DeliveryAddress, Customer
from cust_and_stuff.serializers import CustomerInOrderSerializer, DeliveryAddressSerializer, CustomerSerializer
from .models import DeliveryProvider, DeliveryType, Item, Color, ItemWithColor, ShipmentStatus, Order, \
    OrderItem, Category, ProductImage, Manufacturer, Size, Bucket


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class DeliveryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryType
        fields = ['id', 'name', 'description', 'price']


class DeliveryProviderSerializer(serializers.ModelSerializer):
    delivery_types = DeliveryTypeSerializer(DeliveryType.objects.all(), many=True)

    class Meta:
        model = DeliveryProvider
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.image.url

    class Meta:
        model = ProductImage
        fields = ['created_at', 'updated_at', 'image', 'id']



class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    image = serializers.SerializerMethodField(required=False)
    colors = serializers.SerializerMethodField(required=False)

    def get_colors(self, obj):
        colors = Color.objects.filter(itemwithcolor__item=obj)
        return ColorSerializer(instance=colors, many=True).data

    def get_image(self, obj):
        images = ProductImage.objects.filter(product__item=obj)
        return ProductImageSerializer(instance=images, many=True).data

    class Meta:
        model = Item
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class ClothSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ItemWithColorSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    color = ColorSerializer()
    image = ProductImageSerializer(ProductImage.objects.all(), many=True)
    manufacturer = ManufacturerSerializer()
    size = ClothSizeSerializer(many=True)

    class Meta:
        model = ItemWithColor
        fields = '__all__'


# serializers.py

class ShipmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentStatus
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemWithColorSerializer(ItemWithColor.objects.all(), read_only=True)
    gimage = ImageSerializer(Image.objects.all(), read_only=True)

    prompt = PromptSerializer(Prompt.objects.all(), read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemCreateSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=ItemWithColor.objects.all())
    gimage = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())
    prompt = serializers.PrimaryKeyRelatedField(queryset=Prompt.objects.all())

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    shipping_address = DeliveryAddressSerializer(required=False)
    shipped = ShipmentStatusSerializer(required=False)
    shipping_method = DeliveryTypeSerializer(required=False)
    user = CustomerInOrderSerializer(required=False)
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    shipping_address = serializers.PrimaryKeyRelatedField(queryset=DeliveryAddress.objects.all())
    items = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all(), many=True, required=False)
    shipped = ShipmentStatusSerializer(required=False, read_only=True)
    shipping_method = serializers.PrimaryKeyRelatedField(queryset=DeliveryType.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Order
        fields = '__all__'


class BucketSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = OrderItemSerializer(many=True, required=False)
    class Meta:
        model = Bucket
        fields = '__all__'

