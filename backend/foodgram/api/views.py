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
from .serializers import AchievementSerializer, CatSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    




