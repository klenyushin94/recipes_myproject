from django.contrib import admin
from recipes.models import (FavoriteRecipe, Ingredients, RecipeIngredient,
                            Recipes, ShoppingCartRecipe, Tags,)
from users.models import User


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredient
    min_num = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
    )


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'ingredients',
        'text',
        'cooking_time',
        'pub_date',
    )
    search_fields = (
        'name',
        'cooking_time',
        'tags__name',
        'author__email',
        'ingredients__name'
    )
    list_filter = ('tags', 'author', 'name')
    inlines = (RecipeIngredientAdmin,)

    # @admin.display(description='Теги')
    # def get_tags(self, obj):
    #     return ', '.join([tag.name for tag in obj.tags.all()])

    # @admin.display(description='Ингредиенты')
    # def get_ingredients(self, obj):
    #     return ', '.join(
    #         [ingredient.name for ingredient in obj.ingredients.all()]
    #     )


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user__email', 'recipe__name')


@admin.register(ShoppingCartRecipe)
class ShoppingCartRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user__email', 'recipe__name')
