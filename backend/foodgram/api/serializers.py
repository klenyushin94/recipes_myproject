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
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredients


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        model = Tags


class IngredientsM2MSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'ingredient',
            'ammount',
        )
        model = RecipeIngredient


class ResipesCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientsM2MSerializer(
        many=True,
        source='recipe_ingredient',
    )

    class Meta:
        fields = (
            'id',
            'name',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
        )
        model = Recipes

    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_ingredient')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipes = Recipes.objects.create(author=author, **validated_data)
        for ingredient in ingredients:
            current_ingredient = ingredient.get('ingredient')
            ammount = ingredient.get('ammount')
            recipes.ingredients.add(
                current_ingredient,
                through_defaults={
                    'ammount': ammount,
                }
            )

        for tag in tags:
            recipes.tags.add(tag)

        return recipes


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = FavoriteRecipe


class ShoppingCartRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ShoppingCartRecipe