from django.contrib import admin
from users.models import User
from recipes.models import (
    Recipes, RecipeIngredient, Tags,
    Ingredients, FavoriteRecipe, ShoppingCartRecipe
)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
    )


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'unit',
    )


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color_code',
        'slug',
    )


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'text',
        'cooking_time',
        'pub_date',
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'quantity',
    )


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(ShoppingCartRecipe)
class ShoppingCartRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
