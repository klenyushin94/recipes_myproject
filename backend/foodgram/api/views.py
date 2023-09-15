from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from collections import defaultdict

from djoser.views import UserViewSet

from recipes.models import (
    User,
    Ingredients,
    Tags,
    Recipes,
    FavoriteRecipe,
    ShoppingCartRecipe,
    Subscriptions,
    RecipeIngredient,
    )

from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    RecipesCreateUpdateSerializer,
    RecipesReadSerializer,
    SubscriptionsSerializer,
    CustomUserSerializer,
    CustomUserCreateSerializer,
    RecipesFavoriteShortSerializer,
    ShoppingCartSerializer
)


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomUserSerializer
        return CustomUserCreateSerializer

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            author = get_object_or_404(User, username=author.username)
            subscriptions, created = Subscriptions.objects.get_or_create(
                user=request.user,
                author=author,
            )
            serializer = SubscriptionsSerializer(subscriptions)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            author = get_object_or_404(User, username=author.username)
            Subscriptions.objects.filter(
                user_id=request.user.id,
                author_id=author.pk,
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        subscriptions = Subscriptions.objects.filter(user=request.user)
        serializer = SubscriptionsSerializer(subscriptions, many=True)
        return Response(serializer.data)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = PageNumberPagination


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return RecipesCreateUpdateSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipes, pk=pk)
            favorites = FavoriteRecipe.objects.filter(
                user=request.user,
                recipe=recipe,
            )
            if favorites.exists():
                return Response(
                    {'message': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                favorite = FavoriteRecipe.objects.create(
                    user=request.user,
                    recipe=recipe,
                    )
                serializer = RecipesFavoriteShortSerializer(favorite)
                return Response(serializer.data)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipes, pk=pk)
            favorites = FavoriteRecipe.objects.filter(
                user=request.user,
                recipe=recipe,
                )
            if favorites.exists():
                favorites.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'message': 'Рецепт не найден в избранном'},
                    status=status.HTTP_404_NOT_FOUND
                    )

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipes, pk=pk)
            cart = ShoppingCartRecipe.objects.filter(
                user=request.user,
                recipe=recipe,
            )
            if cart.exists():
                return Response(
                    {'message': 'Рецепт уже добавлен в список продуктов'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                cart = ShoppingCartRecipe.objects.create(
                    user=request.user,
                    recipe=recipe,
                    )
                serializer = ShoppingCartSerializer(cart)
                return Response(serializer.data)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipes, pk=pk)
            cart = ShoppingCartRecipe.objects.filter(
                user=request.user,
                recipe=recipe,
                )
            if cart.exists():
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'message': 'Рецепт не найден списке продуктов'},
                    status=status.HTTP_404_NOT_FOUND
                    )

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        user = request.user
        cart_items = ShoppingCartRecipe.objects.filter(user=user)
        ingredients_totals = defaultdict(int)
        for cart_item in cart_items:
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=cart_item.recipe)
            for recipe_ingredient in recipe_ingredients:
                ingredient = recipe_ingredient.ingredient
                ingredients_totals[ingredient.name] += recipe_ingredient.amount
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.pdf"'
        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)
        y = 100
        for ingredient, amount in ingredients_totals.items():
            p.drawString(100, y, f"{ingredient} ({ingredient}) - {amount}")
            y += 20
        p.showPage()
        p.save()
        return response
