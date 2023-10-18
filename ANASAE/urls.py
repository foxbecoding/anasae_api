"""ANASAE_Api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('brands.ecosystem.app.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('categories.ecosystem.app.urls')),
    path('api/', include('products.ecosystem.app.urls')),
    path('api/', include('users.ecosystem.app.urls')),
    path('api/', include('users.ecosystem.auth.urls')),
    path('api/', include('users.ecosystem.security.urls')),
    path('api/', include('sliders.ecosystem.admin.urls')),
    path('api/', include('sliders.ecosystem.app.urls'))
]