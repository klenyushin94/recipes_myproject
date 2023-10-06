from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import constraints
from users.models import User

from .constants import COLOR_MAX_LENGTH, NAME_MAX_LENGTH


class Ingredients(models.Model):
    """Модель ингредиента."""
    name = models.CharField(
        'Название ингредиента',
        max_length=NAME_MAX_LENGTH
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=NAME_MAX_LENGTH,
        unique=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=NAME_MAX_LENGTH
    )
    color = models.CharField(
        'Цветовой код',
        max_length=COLOR_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Формат цвета не соответствует HEX')]
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название блюда',
        max_length=NAME_MAX_LENGTH,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    text = models.TextField('Текст описания блюда')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.IntegerField(
        'Время приготовления блюда',
        validators=(
            MinValueValidator(
                1,
                message='Время приготовления должно быть больше 0'),)
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Промежуточная модель для связи рецептов и ингредиентов."""
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
    )
    amount = models.IntegerField(
        'Количество',
        default=1,
        validators=(
            MinValueValidator(
                1,
                message='Количество ингредиента должно быть больше 0'),)
    )

    class Meta:
        verbose_name = 'Граммовка ингредиента'
        verbose_name_plural = 'Граммовки ингридиентов'

    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name}"


class FavoriteRecipe(models.Model):
    """Модель для любимых блюд."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"


class ShoppingCartRecipe(models.Model):
    """Модель для списка покупок."""
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
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shoppingcart_recipe'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"


class Subscriptions(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )

    class Meta:
        verbose_name_plural = 'Подписка'
        constraints = [
            constraints.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='author_not_equals_user'
            ),
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscription',
            )
        ]
