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
    SubscriptionsViewSet,
    SubscribeViewSet,
)

router1 = routers.DefaultRouter()
router1.register(r'tags', TagsViewSet)
router1.register(r'recipes', RecipesViewSet)
router1.register(r'ingredients', IngredientsViewSet)
router1.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router1.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
