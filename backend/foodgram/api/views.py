from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

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
    ShoppingCartRecipeSerializer
)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = PageNumberPagination


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = ResipesCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer


class ShoppingCartRecipeViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCartRecipe.objects.all()
    serializer_class = ShoppingCartRecipeSerializer
