from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reviews.views import CategoryViewSet, GenreViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
