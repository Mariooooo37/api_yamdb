from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Roles(models.TextChoices):
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        USER = 'user'

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=Roles.choices,
        default=Roles.USER
    )
    '''Добавляем поле bio'''
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]
