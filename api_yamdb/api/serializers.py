import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment, User


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


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

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего года!')
        return value

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
        # убрал дефолтные значения для author и title, по идее, мы их должны
        # прописывать, только если у нас есть кастомная валидация по этим полям
        # в сериализаторе.
        # а обычную валидацию из коробки оно пройдет, т.к. read_only они оба
        # а вьюха значения этих полей уже подсунет после валидации
        # короче, по сути я валидацию перенес во вьюху для Review, глянь там
    )

    def validate_score(self, value):
        if not (0 <= value <= 10):
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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)
