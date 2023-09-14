import base64

from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.core.files.base import ContentFile

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


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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


class RecipeIngredientsReadSerializer(serializers.ModelSerializer):
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


class RecipesCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientsM2MSerializer(
        many=True,
        source='recipe_ingredient',
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = (
            'id',
            'name',
            'text',
            'ingredients',
            'tags',
            'image',
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
            amount = ingredient.get('amount')
            recipes.ingredients.add(
                current_ingredient,
                through_defaults={
                    'amount': amount,
                }
            )

        for tag in tags:
            recipes.tags.add(tag)

        return recipes


class RecipesReadSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientsReadSerializer(source='recipe_ingredient', many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
        )
        model = Recipes

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        recipe = obj.id
        is_favorited = FavoriteRecipe.objects.filter(
            user=user,
            recipe=recipe
            ).exists()
        return is_favorited


class ShoppingCartRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ShoppingCartRecipe


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Subscriptions


class RecipesFavoriteShortSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        fields = (
            'id',
            'name',
            'cooking_time',
        )
        model = FavoriteRecipe


class RecipesShortSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'cooking_time',
        )
        model = Recipes


class SubscriptionsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email')
    id = serializers.IntegerField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        model = Subscriptions

    def get_is_subscribed(self, obj):
        user = obj.user
        author = obj.author
        is_subscribed = Subscriptions.objects.filter(
            user=user,
            author=author
            ).exists()
        return is_subscribed

    def get_recipes(self, obj):
        author = obj.author
        recipes = Recipes.objects.filter(author=author)
        serializer = RecipesShortSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        author = obj.author
        recipes_count = Recipes.objects.filter(author=author).count()
        return recipes_count
