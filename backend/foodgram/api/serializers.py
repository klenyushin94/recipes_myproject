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
    name = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'name',
            'amount',
        )
        model = RecipeIngredient


class ResipesCreateUpdateSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    tags = TagsSerializer(many=True)
    ingredients = IngredientsM2MSerializer(
        many=True,
        source='recipe_ingredient',
    )

    class Meta:
        fields = (
            'id',
            'author',
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
        recipes = Recipes.objects.create(**validated_data)

        for ingredient in ingredients:
            current_ingredient = ingredient.get('ingredient')
            amount = ingredient.get('amount')
            recipes.ingredients.add(
                current_ingredient,
                through_defaults={
                    'ammout': amount,
                }
            )
      
        for tag in tags:
            tag, status = Tags.objects.get_or_create(**tags)
            recipes.tags.add(tag)

        return recipes





# class RecipesSerializer(serializers.ModelSerializer):
#     author = SlugRelatedField(slug_field='username', read_only=True)
#     tags = TagsSerializer(many=True)

#     class Meta:
#         fields = (
#             'id',
#             'author',
#             'name',
#             'text',
#             'ingredients',
#             'tags',
#             'cooking_time',
#         )
#         model = Recipes

#     def create(self, validated_data):
#         tags = validated_data.pop('tags')
#         recipes = Recipes.objects.create(**validated_data)

#         for tag in tags:
#             tag, status = Tags.objects.get_or_create(**tags)
#             recipes.tags.add(tag)
#         return recipes


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