from rest_framework import routers
from django.contrib import admin
from django.urls import include, path

# from recipes.views import AchievementViewSet, CatViewSet


# router = routers.DefaultRouter()
# # router.register(r'cats', CatViewSet)
# # router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
 #   path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),  # Работа с пользователями.
    path('api/auth/', include('djoser.urls.authtoken')),  # Работа с токенами.
]
