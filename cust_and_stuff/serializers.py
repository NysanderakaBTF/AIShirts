from rest_framework import serializers
from .models import DeliveryAddress, Customer


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'

    def create(self, validated_data):
        # Try to find an existing delivery address with the same fields
        existing_delivery_addresses = DeliveryAddress.objects.filter(
            street_address=validated_data.get('street_address'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            zip_code=validated_data.get('zip_code'),
            country=validated_data.get('country')
        )
        if existing_delivery_addresses.exists():
            # Use the existing delivery address if one exists
            delivery_address = existing_delivery_addresses.first()
        else:
            # Create a new delivery address if one doesn't exist
            delivery_address = super().create(validated_data)
        return delivery_address


class CustomerSerializer(serializers.ModelSerializer):
    delivery_address = DeliveryAddressSerializer(required=False, many=True)

    def update(self, instance, validated_data):
        # delivery_addresses_data = self.initial_data.pop('delivery_address', None)
        # self.validated_data.pop('delivery_address', None)
        delivery_addresses_data = validated_data.pop('delivery_address', [])
        ids_raw = self.initial_data.get('delivery_address', None)
        if ids_raw is not None:
            delivery_address_ids = [i['id'] for i in ids_raw]
        if delivery_addresses_data is not None:
            # Get all existing delivery addresses for the customer
            existing_delivery_addresses = instance.delivery_address.all()
            # Get the IDs of the delivery addresses that were passed in the request
            # delivery_address_ids = [i['id'] for i in delivery_addresses_data]
            # Remove any delivery addresses that were not specified in the request
            for delivery_address in existing_delivery_addresses:
                if delivery_address.id not in delivery_address_ids:
                    instance.delivery_address.remove(delivery_address)
            # Add or update the remaining delivery addresses
            delivery_addresses = DeliveryAddress.objects.filter(id__in=delivery_address_ids)
            instance.delivery_address.set(delivery_addresses)
            instance.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number']
