from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from users.models import User
from recipes.models import (
    Ingredients,
    Tags,
    Recipes,
    RecipeIngredient,
    FavoriteRecipe,
    ShoppingCartRecipe,
)


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredients


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tags


class RecipesSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Recipes


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = RecipeIngredient


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = FavoriteRecipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = FavoriteRecipe


class ShoppingCartRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ShoppingCartRecipe