from django.urls import path
from .views import DeliveryProviderViewSet, DeliveryTypeViewSet, CategoryViewSet, ItemViewSet, \
    ProductImageViewSet, ColorViewSet, ItemWithColorViewSet, ShipmentStatusViewSet, OrderViewSet, OrderItemViewSet, \
    GetOrdersForUser

urlpatterns = [
    path('delivery-providers/', DeliveryProviderViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='deliveryprovider-list'),
    path('delivery-providers/<int:pk>/', DeliveryProviderViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='deliveryprovider-detail'),
    path('delivery-types/', DeliveryTypeViewSet.as_view({'get': 'list', 'post': 'create'}), name='deliverytype-list'),
    path('delivery-types/<int:pk>/', DeliveryTypeViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='deliverytype-detail'),
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('categories/<int:pk>/',
         CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='category-detail'),
    path('items/', ItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='item-list'),
    path('items/<int:pk>/',
         ItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='item-detail'),
    path('product-images/', ProductImageViewSet.as_view({'get': 'list', 'post': 'create'}), name='productimage-list'),
    path('product-images/<int:pk>/', ProductImageViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='productimage-detail'),
    path('colors/', ColorViewSet.as_view({'get': 'list', 'post': 'create'}), name='color-list'),
    path('colors/<int:pk>/',
         ColorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='color-detail'),
    path('items-with-color/', ItemWithColorViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='itemwithcolor-list'),
    path('items-with-color/<int:pk>/', ItemWithColorViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='itemwithcolor-detail'),
    path('shipment-statuses/', ShipmentStatusViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='shipmentstatus-list'),
    path('shipment-statuses/<int:pk>/', ShipmentStatusViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='shipmentstatus-detail'),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('orders/user/', GetOrdersForUser.as_view(), name='get_orders_for_user'),
    path('orders/<int:pk>/',
         OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='order-detail'),
    path('orders/<int:pk>/add-item/', OrderViewSet.as_view({'post': 'add_item'}), name='order-add-item'),
    path('order-items/', OrderItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='orderitem-list'),
    path('order-items/<int:pk>/',
         OrderItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='orderitem-detail'),
]
