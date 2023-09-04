from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.db import models


# class UserCustomManager(UserManager):
#     def _create_user(self, email, password,  username=None, **extra_fields):
#         """
#         Create and save a user with the given username, email, and password.
#         """
#         if not username:
#             raise ValueError('The given username must be set')
#         email = self.normalize_email(email)
#         username = self.model.normalize_username(username)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, username=None, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(username, email, password, **extra_fields)


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

    # REQUIRED_FIELDS = []
    # objects = UserCustomManager()
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return f'{self.username} ({self.email})'


#User = get_user_model()
