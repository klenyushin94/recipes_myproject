from django.contrib import admin
from django.db.models import Count
from recipes.models import (FavoriteRecipe, Ingredients, RecipeIngredient,
                            Recipes, ShoppingCartRecipe, Tags)
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
        'favorite_count',
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(favorite_count=Count('favorite_recipes'))
        return queryset

    def favorite_count(self, obj):
        return obj.favorite_count

    favorite_count.short_description = 'Добавления в избранное'


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
