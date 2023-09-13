from rest_framework import routers
from django.contrib import admin
from django.urls import include, path

from api.views import (
    UserViewSet,
    IngredientsViewSet,
    TagsViewSet,
    RecipesViewSet,
    FavoriteRecipeViewSet,
    ShoppingCartRecipeViewSet,
    )

router1 = routers.DefaultRouter()
router1.register(r'tags', TagsViewSet, basename='tags')
router1.register(r'recipes', RecipesViewSet, basename='recipes')
router1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router1.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
