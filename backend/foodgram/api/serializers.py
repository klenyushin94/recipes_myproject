import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (FavoriteRecipe, Ingredients, RecipeIngredient,
                            Recipes, ShoppingCartRecipe, Subscriptions, Tags)
from rest_framework import serializers
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)


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
        if user.is_anonymous or not user.id:
            return False
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
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
    )

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
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())

    class Meta:
        fields = (
            'id',
            'amount',
        )
        model = RecipeIngredient


class RecipesCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientsM2MSerializer(
        many=True,
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = (
            'name',
            'text',
            'ingredients',
            'tags',
            'image',
            'cooking_time',
        )
        model = Recipes

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                "Ingredients field cannot be empty.",
            )
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipes = Recipes.objects.create(author=author, **validated_data)
        recipes.save()
        for ingredient in ingredients:
            current_ingredient = ingredient.get('id')
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

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        tags_data = validated_data.pop('tags', [])
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time,
        )
        instance.ingredients.clear()
        for ingredient_data in ingredients_data:
            ingredient = ingredient_data['id']
            amount = ingredient_data['amount']
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient=ingredient,
                amount=amount
            )
        instance.tags.clear()
        for tag_data in tags_data:
            tag = tag_data
            instance.tags.add(tag)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipesReadSerializer(
            instance,
            context=self.context
        ).data


class RecipesReadSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientsReadSerializer(
        source='recipe_ingredient',
        many=True
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

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
            'is_in_shopping_cart',
        )
        model = Recipes

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or not user.id:
            return False
        recipe = obj.id
        is_favorited = FavoriteRecipe.objects.filter(
            user=user,
            recipe=recipe
        ).exists()
        return is_favorited

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or not user.id:
            return False
        recipe = obj.id
        is_in_shopping_cart = ShoppingCartRecipe.objects.filter(
            user=user,
            recipe=recipe
        ).exists()
        return is_in_shopping_cart

    # def get_is_favorited(self, obj):
    #     user = self.context['request'].user
    #     recipe = obj.id
    #     is_favorited = FavoriteRecipe.objects.filter(
    #         user=user,
    #         recipe=recipe
    #     ).exists()
    #     return is_favorited

    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context['request'].user
    #     recipe = obj.id
    #     is_in_shopping_cart = ShoppingCartRecipe.objects.filter(
    #         user=user,
    #         recipe=recipe
    #     ).exists()
    #     return is_in_shopping_cart


class RecipesFavoriteShortSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = Base64ImageField(
        source='recipe.image',
        required=False,
        allow_null=True
    )
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        model = FavoriteRecipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = Base64ImageField(
        source='recipe.image',
        required=False,
        allow_null=True,
    )
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        model = ShoppingCartRecipe


class RecipesShortSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'cooking_time',
            'image',
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
