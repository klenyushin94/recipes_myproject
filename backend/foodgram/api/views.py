import re
from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (FavoriteRecipe, Ingredients, RecipeIngredient,
                            Recipes, ShoppingCartRecipe, Subscriptions, Tags,
                            User)
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .serializers import (CustomUserCreateSerializer, CustomUserSerializer,
                          IngredientsSerializer, RecipesCreateUpdateSerializer,
                          RecipesFavoriteShortSerializer,
                          RecipesReadSerializer, SetPasswordSerializer,
                          ShoppingCartSerializer, SubscriptionsSerializer,
                          TagsSerializer)


class UserPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 100


class SubscriptionsPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = UserPagination

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        if re.match(r'^[A-Za-z0-9]+$', username):
            return super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomUserSerializer
        return CustomUserCreateSerializer

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            author = get_object_or_404(User, id=id)
            subscriptions, created = Subscriptions.objects.get_or_create(
                user=request.user,
                author=author,
            )
            serializer = SubscriptionsSerializer(subscriptions)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            author = get_object_or_404(User, id=id)
            Subscriptions.objects.filter(
                user_id=request.user.id,
                author_id=author.pk,
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        subscriptions = Subscriptions.objects.filter(user=request.user)
        paginator = SubscriptionsPagination()
        result_page = paginator.paginate_queryset(subscriptions, request)
        serializer = SubscriptionsSerializer(result_page, many=True)
        recipes_limit = request.GET.get('recipes_limit', None)
        if recipes_limit:
            for subscription in serializer.data:
                subscription['recipes'] = (
                    subscription['recipes'][:int(recipes_limit)]
                )
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        if not user.check_password(current_password):
            return Response(
                {'error': 'Invalid current password.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {'message': 'Password successfully changed.'},
            status=status.HTTP_200_OK
        )


class IngredientsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('^name', )


class TagsViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Tags.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [permissions.AllowAny]
    #     return super().get_permissions()

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
            recipe_ingredients = RecipeIngredient.objects.filter(
                recipe=cart_item.recipe,
            )
            for recipe_ingredient in recipe_ingredients:
                ingredient = recipe_ingredient.ingredient
                ingredients_totals[ingredient.name] += recipe_ingredient.amount
        MyFontObject = ttfonts.TTFont('Arial', './media/arial.ttf')
        pdfmetrics.registerFont(MyFontObject)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; '
            'filename="shopping_cart.pdf"'
        )
        p = canvas.Canvas(response)
        p.setFont("Arial", 12)
        p.setFont("Arial", 14)
        p.drawString(100, 800, _("Cписок продуктов"))
        p.setFont("Arial", 12)
        y = 750
        for ingredient, amount in ingredients_totals.items():
            measurement_unit = Ingredients.objects.get(name=ingredient)
            measurement_unit = measurement_unit.measurement_unit
            p.drawString(
                100,
                y,
                f"{ingredient} ({measurement_unit}) - {amount}")
            y -= 20
        p.showPage()
        p.save()
        return response
