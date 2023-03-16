from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reviews.views import CategoryViewSet, GenreViewSet, TitleViewSet
from reviews.views import ReviewViewSet, CommentViewSet

v1_router = DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
