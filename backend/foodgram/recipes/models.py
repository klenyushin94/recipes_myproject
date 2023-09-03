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
        #'username',
        'email',
        'first_name',
        'last_name',
        'password',
    ]

    # USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = []
    # objects = UserCustomManager()
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return f'{self.username} ({self.email})'


#User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField('Название ингредиента', max_length=50)
    unit = models.CharField('Единицы измерения', max_length=20, unique=False)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Название тега', max_length=50)
    color_code = models.CharField('Цветовой код', max_length=7)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название блюда',
        max_length=50,
    )
    # image = models.ImageField('Картинка', upload_to='posts/', blank=True)
    text = models.TextField('Текст описания блюда')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
        )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.IntegerField('Время приготовления блюда')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
    )
    quantity = models.DecimalField(
        'Количество',
        max_digits=5,
        decimal_places=2
    )

    class Meta:
        verbose_name = 'граммовку'
        verbose_name_plural = 'Граммовки ингридиентов'

    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name}"


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь'
        )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Рецепт'
        )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"


class ShoppingCartRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes',
        verbose_name='Пользователь'
        )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='added_to_cart_by',
        verbose_name='Рецепт'
        )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"
