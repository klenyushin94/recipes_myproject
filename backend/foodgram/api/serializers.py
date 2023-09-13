from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from users.models import User
from recipes.models import (
    Ingredients,
    Tags,
    Recipes,
    RecipeIngredient,
    FavoriteRecipe,
    ShoppingCartRecipe,
    Subscriptions
)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        author = obj
        is_subscribed = Subscriptions.objects.filter(
            user=user,
            author=author
        ).exists()
        return is_subscribed


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        model = User


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        model = Ingredients


class ResipeIngredientsReadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'amount',
            'measurement_unit',
        )


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
            'ingredient',
            'amount',
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
            ammount = ingredient.get('amount')
            recipes.ingredients.add(
                current_ingredient,
                through_defaults={
                    'amount': ammount,
                }
            )

        for tag in tags:
            recipes.tags.add(tag)

        return recipes


class ResipesReadSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = ResipeIngredientsReadSerializer(source='recipe_ingredient', many=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'text',
            'cooking_time',
        )
        model = Recipes


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = FavoriteRecipe


class ShoppingCartRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ShoppingCartRecipe


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Subscriptions


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Subscriptions
