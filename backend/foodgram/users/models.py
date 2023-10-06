import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_username(value):
    pattern = r'^[a-zA-Z0-9]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Имя пользователя может содержать только буквы и цифры.'
        )


class User(AbstractUser):
    """Модель кастомного пользователя."""
    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text='Введите e-mail',
        unique=True,
        blank=False,
        max_length=254,
    )
    username = models.CharField(
        verbose_name='Логин',
        help_text='Введите username',
        unique=True,
        blank=False,
        max_length=150,
        validators=[validate_username],
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
    is_subscribed = models.BooleanField(
        verbose_name='Подписка',
        default=False,
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
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.username} ({self.email})'
