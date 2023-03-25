from django.db import models

from user.models import User
from api.validators import validate_year


class Genre(models.Model):
    name = models.CharField(verbose_name='Жанр', max_length=256)
    slug = models.SlugField(verbose_name='Slug', max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=256)
    slug = models.SlugField(verbose_name='Slug', max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(verbose_name='Имя', max_length=256, db_index=True)
    year = models.IntegerField(
        verbose_name='Год', db_index=True, validators=(validate_year, ))
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True,
        verbose_name='Жанр',
        # В полях ManyToManyField null=True по умолчанию)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Связь жанра с произведением'
        verbose_name_plural = 'Связи жанра с произведением'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField('Описание')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews1',
        verbose_name='Автор',
    )
    score = models.IntegerField('Оценка')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_review'
            )]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text
