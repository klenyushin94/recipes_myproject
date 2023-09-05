from rest_framework import routers
from django.contrib import admin
from django.urls import include, path

from api.views import (
    IngredientsViewSet,
    TagsViewSet,
    RecipesViewSet,
    FavoriteRecipeViewSet,
    ShoppingCartRecipeViewSet,
)

router = routers.DefaultRouter()
router.register(r'tags', TagsViewSet)
router.register(r'recipes', RecipesViewSet)
router.register(r'ingredients', IngredientsViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),  # Работа с пользователями.
    path('api/auth/', include('djoser.urls.authtoken')),  # Работа с токенами.
]
