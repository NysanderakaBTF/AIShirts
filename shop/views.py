from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import DeliveryProvider, DeliveryType, DeliveryAddress, Category, Item, ProductImage, Color, ItemWithColor, \
    ShipmentStatus, Order, OrderItem
from .permissions import ReadOnlyOrStaffOnlyPermission
from .serializers import DeliveryProviderSerializer, DeliveryTypeSerializer, \
    CategorySerializer, ItemSerializer, ProductImageSerializer, ColorSerializer, ItemWithColorSerializer, \
    ShipmentStatusSerializer, OrderSerializer, OrderItemSerializer


class DeliveryProviderViewSet(viewsets.ModelViewSet):
    queryset = DeliveryProvider.objects.all()
    serializer_class = DeliveryProviderSerializer
    permission_classes = [ReadOnlyOrStaffOnlyPermission]


class DeliveryTypeViewSet(viewsets.ModelViewSet):
    queryset = DeliveryType.objects.all()
    serializer_class = DeliveryTypeSerializer
    permission_classes = [ReadOnlyOrStaffOnlyPermission]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrStaffOnlyPermission]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [ReadOnlyOrStaffOnlyPermission]


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [ReadOnlyOrStaffOnlyPermission]


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [ReadOnlyOrStaffOnlyPermission]


class ItemWithColorViewSet(viewsets.ModelViewSet):
    queryset = ItemWithColor.objects.all()
    serializer_class = ItemWithColorSerializer
    permission_classes = [ReadOnlyOrStaffOnlyPermission]


class ShipmentStatusViewSet(viewsets.ModelViewSet):
    queryset = ShipmentStatus.objects.all()
    serializer_class = ShipmentStatusSerializer
    permission_classes = [ReadOnlyOrStaffOnlyPermission]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class GetOrdersForUser(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
