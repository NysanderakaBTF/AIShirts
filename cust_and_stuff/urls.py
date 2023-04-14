from allauth.account.views import ConfirmEmailView
from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetConfirmView, PasswordChangeView
)
from .views import (
    CustomerListCreateAPIView, CustomerRetrieveUpdateDestroyAPIView,
    CustomerGenerationCountAPIView, DeliveryAddressViewSet,
)

urlpatterns = [
    # path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/registration/', include('dj_rest_auth.registration.urls'), name='account_signup'),
    path('accounts/registration/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('accounts/logout/', LogoutView.as_view(), name='rest_logout'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('accounts/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/generation-count/', CustomerGenerationCountAPIView.as_view(),
         name='customer_generation_count'),
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer_list'),
    path('delivery-addresses/', DeliveryAddressViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='deliveryaddress-list'),
    path('delivery-addresses/<int:pk>/', DeliveryAddressViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='deliveryaddress-detail'),
]
