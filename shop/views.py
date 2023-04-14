from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DeliveryProvider, DeliveryType, DeliveryAddress, Category, Item, ProductImage, Color, ItemWithColor, \
    ShipmentStatus, Order, OrderItem, Bucket
from .permissions import ReadOnlyOrStaffOnlyPermission, ModifyOrdersPermission, IsOwnerOrStaffOnly
from .serializers import DeliveryProviderSerializer, DeliveryTypeSerializer, \
    CategorySerializer, ItemSerializer, ProductImageSerializer, ColorSerializer, ItemWithColorSerializer, \
    ShipmentStatusSerializer, OrderSerializer, OrderItemSerializer, OrderCreateSerializer, BucketSerializer, \
    OrderItemCreateSerializer


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


class OrderViewSet(APIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, ModifyOrdersPermission]
    '''
    reqest example:
    
    '''

    def post(self, request, *args, **kwargs):
        data = request.data
        data.setdefault('user', request.user)
        if 'shipped' not in data.keys():
            data.setdefault('shipped', ShipmentStatus.objects.get(pk=1))

        if 'items' in data.keys():
            bucket = Bucket.objects.get(user=request.user)
            bucket.items.set(filter(lambda x: x.pk not in data['items'], bucket.items.all()))
            bucket.save()

        pk = request.user.id
        data['user'] = pk
        serializer = OrderCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(instance=orders, many=True)
        print(serializer.__dict__)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if request.user.is_staff:
            order = get_object_or_404(Order, pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        if request.user.is_staff:
            order = get_object_or_404(Order, pk=pk)
            serializer = OrderSerializer(instance=order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class GetOrdersForUser(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class BucketAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrStaffOnly]
    def post(self, request, pk):
        try:
            bucket = Bucket.objects.get(user=request.user)
        except Bucket.DoesNotExist:
            bucket_ser = BucketSerializer(data={'user':request.user.pk})
            bucket_ser.is_valid(raise_exception=True)
            bucket = bucket_ser.save()
        item = ItemWithColor.objects.get(pk=pk)
        data = request.data
        data.setdefault('item', item.pk)
        or_item_serializer = OrderItemCreateSerializer(data=data)
        or_item_serializer.is_valid(raise_exception=True)
        bucket_item = or_item_serializer.save()
        bucket.items.add(bucket_item)
        bucket.total += bucket_item.quantity * bucket_item.item.price
        bucket.save()
        return Response(BucketSerializer(instance=bucket).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            bucket = Bucket.objects.get(user=request.user)
        except Bucket.DoesNotExist:
            bucket_ser = BucketSerializer(data={'user':request.user.pk})
            bucket_ser.is_valid(raise_exception=True)
            bucket = bucket_ser.save()
            return Response(BucketSerializer(instance=bucket).data, status=status.HTTP_201_CREATED)
        bucket = get_object_or_404(Bucket, user=request.user)
        serializer = BucketSerializer(instance=bucket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        bucket = get_object_or_404(Bucket, user=request.user)
        serializer = BucketSerializer(instance=bucket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        bucket = get_object_or_404(Bucket, user=request.user)
        bucket.items.remove(get_object_or_404(OrderItem, pk=pk))
        bucket.total -= get_object_or_404(OrderItem, pk=pk).quantity * get_object_or_404(OrderItem, pk=pk).item.price
        bucket.save()
        return Response(BucketSerializer(instance=bucket).data, status=status.HTTP_200_OK)




