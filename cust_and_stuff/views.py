from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import generics, permissions, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsCurrentUserOrStaff
from .models import Customer, DeliveryAddress
from .serializers import CustomerSerializer, DeliveryAddressSerializer


class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    #TODO: permission that user cat updait himself
    permission_classes = (IsCurrentUserOrStaff,)

    def patch(self, request, pk):
        instance = get_object_or_404(Customer, pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk):
        instance = get_object_or_404(Customer, pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomerGenerationCountAPIView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAdminUser,)

    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.generation_count += 1
        customer.save()
        serializer = self.get_serializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]
