from django.db import models
from users.models import User


class Ingredients(models.Model):
    name = models.CharField('Название ингредиента', max_length=50)
    measurement_unit = models.CharField('Единицы измерения', max_length=20, unique=False)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField('Название тега', max_length=50)
    color = models.CharField('Цветовой код', max_length=7)
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
        verbose_name='Ингредиенты',
        )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.IntegerField('Время приготовления блюда')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
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
