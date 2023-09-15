from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from api.views import (
    UserViewSet,
    IngredientsViewSet,
    TagsViewSet,
    RecipesViewSet,
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

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
        )
