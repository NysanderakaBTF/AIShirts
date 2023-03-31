from rest_framework import serializers
from .models import DeliveryAddress, Customer


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    delivery_address = DeliveryAddressSerializer()

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerInOrderSerializer(serializers.ModelSerializer):
    delivery_address = DeliveryAddressSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'email', 'first_name', 'last_name', 'delivery_address']
