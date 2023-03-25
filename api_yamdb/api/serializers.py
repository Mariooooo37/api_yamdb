import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.forms import ValidationError

from reviews.models import Category, Genre, Title, Review, Comment
from user.models import User

MIN_SCORE = 0
MAX_SCORE = 10


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise ValidationError(
                'Имя пользователя содержит запрещенные символы'
            )
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class UserSerializer(RegisterDataSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(RegisterDataSerializer):

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150
    )
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = (representation['rating']
                                    if representation['rating'] else None)
        return representation


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=False,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )

    def validate_score(self, value):
        if not (MIN_SCORE <= value <= MAX_SCORE):
            raise serializers.ValidationError('Оценка не по 10-бальной шкале!')
        return value

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id',
    )

    class Meta:
        model = Comment
        fields = '__all__'
