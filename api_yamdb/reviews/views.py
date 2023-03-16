from rest_framework import viewsets, mixins

from reviews.models import Category, Genre, Title
from reviews.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    # Пермишены


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    # Пермишены


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # Пермишены
