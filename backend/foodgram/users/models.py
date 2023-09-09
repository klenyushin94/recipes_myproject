from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.db import models


class User(AbstractUser):
    """Модель кастомного пользователя."""
    email = models.EmailField(
        verbose_name='E-mail',
        help_text='Введите e-mail',
        unique=True,
        blank=False,
        max_length=254,
    )
    username = models.CharField(
        verbose_name='Username',
        help_text='Введите username',
        unique=True,
        blank=False,
        max_length=150,
        error_messages={
            'unique': 'Пользователь с таким username уже создан!',
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        blank=False,
        help_text='Введите имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        blank=False,
        help_text='Введите фамилию',
        max_length=150,
    )

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return f'{self.username} ({self.email})'
