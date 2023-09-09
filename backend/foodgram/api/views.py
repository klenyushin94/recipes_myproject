from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS

from users.models import User
from recipes.models import (
    Ingredients,
    Tags,
    Recipes,
    RecipeIngredient,
    FavoriteRecipe,
    ShoppingCartRecipe,
)
from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    ResipesCreateUpdateSerializer,
    FavoriteRecipeSerializer,
    ShoppingCartRecipeSerializer,
    ResipesReadSerializer
)


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
        # if self.request.method == SAFE_METHODS:
        if self.request.method == 'GET':
            return ResipesReadSerializer
        return ResipesCreateUpdateSerializer


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer


class ShoppingCartRecipeViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCartRecipe.objects.all()
    serializer_class = ShoppingCartRecipeSerializer
