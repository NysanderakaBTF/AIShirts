from rest_framework import serializers

from aiintegration.serializers import ImageSerializer, PromptSerializer
from cust_and_stuff.serializers import CustomerInOrderSerializer, DeliveryAddressSerializer
from .models import DeliveryProvider, DeliveryType, Item, Color, ItemWithColor, ShipmentStatus, Order, \
    OrderItem, Category, ProductImage


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
    image = ProductImageSerializer(ProductImage.objects.all(), many=True)
    category = CategorySerializer(many=True)

    class Meta:
        model = Item
        fields = '__all__'

    def get_image(self, obj):
        return obj.image.url


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class ItemWithColorSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    color = ColorSerializer()
    image = ProductImageSerializer(ProductImage.objects.all(), many=True)

    class Meta:
        model = ItemWithColor
        fields = '__all__'


class ShipmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentStatus
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemWithColorSerializer()
    gimage = ImageSerializer()
    prompt = PromptSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemSerializer(many=True)
    shipping_address = DeliveryAddressSerializer()
    shipped = ShipmentStatusSerializer()
    shipping_method = DeliveryTypeSerializer()
    user = CustomerInOrderSerializer()
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = '__all__'
