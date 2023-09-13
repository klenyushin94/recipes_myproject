from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.models import User

from djoser.views import UserViewSet

from recipes.models import (
    User,
    Ingredients,
    Tags,
    Recipes,
    FavoriteRecipe,
    ShoppingCartRecipe,
    Subscriptions,
)
from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    ResipesCreateUpdateSerializer,
    FavoriteRecipeSerializer,
    ShoppingCartRecipeSerializer,
    ResipesReadSerializer,
    SubscribeSerializer,
    SubscriptionsSerializer,
    CustomUserSerializer,
    CustomUserCreateSerializer,
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
        author = self.get_object()
        if request.method == 'POST':
            author = get_object_or_404(User, username=author.username)
            Subscriptions.objects.get_or_create(
                user=request.user,
                author=author,
            )
            return Response({'message': 'Подписка создана'})
        elif request.method == 'DELETE':
            author = get_object_or_404(User, username=author.username)
            Subscriptions.objects.filter(
                user_id=request.user.id,
                author_id=author.pk,
            ).delete()
            return Response({'message': 'Подписка удалена'})

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
            return ResipesReadSerializer
        return ResipesCreateUpdateSerializer


class SubscriptionsViewSet(viewsets.ViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer

    # def list(self, request):
    #     serializer = self.serializer_class(
    #         self.queryset,
    #         many=True,
    #         context={'request': request}
    #     )
    #     return Response(serializer.data)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return self.request.user.follower.all()

    # def destroy(self, request, id=None):
    #     # Логика отписки пользователя
    #     user_id = id
    #     # Ваш код для обработки отписки пользователя
    #     return Response({'message': f'User {user_id} has been unsubscribed'})


class SubscribeViewSet(viewsets.ViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscribeSerializer


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer


class ShoppingCartRecipeViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCartRecipe.objects.all()
    serializer_class = ShoppingCartRecipeSerializer
