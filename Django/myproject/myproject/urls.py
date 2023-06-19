"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from myapp.views import MyAPIView, AlbumView, TrackView
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('api/myapi/<int:pk>/', MyAPIView.as_view(), name='myapi-detail'),
    path('api/myapi/', MyAPIView.as_view(), name='myapi-list'),

    path('api/albums/', AlbumView.as_view(), name='album-list'),
    path('api/albums/<int:pk>/', AlbumView.as_view(), name='album-detail'),
    path('api/albums/<int:album_pk>/tracks/', TrackView.as_view(), name='track-list'),
    path('api/albums/<int:album_pk>/tracks/<int:track_pk>/', TrackView.as_view(), name='track-detail'),

    path('api/login', TokenObtainPairView.as_view(), name='login token'),
    path('api/login/refresh', TokenRefreshView.as_view(), name='refresh login token'),
    path('api/login/verify', TokenVerifyView.as_view(), name='verify login token'),

    path('', include('myapp.urls')),
]
