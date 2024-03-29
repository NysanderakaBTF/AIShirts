"""AIShirts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from cust_and_stuff.views import FacebookLogin, TwitterLogin, GoogleLogin

#TODO:add auth by google/twitter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),




    path('shop/', include('shop.urls')),
    path('ai/', include('aiintegration.urls')),
    path('users/', include('cust_and_stuff.urls')),
    # path('media/<path:path>', serve, name='serve_static_file'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
