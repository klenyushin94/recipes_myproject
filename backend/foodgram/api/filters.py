from django_filters import rest_framework as filters
from recipes.models import Ingredients, Recipes, Tags


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredients
        fields = ['name', ]


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    author = filters.NumberFilter(field_name='author__id')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorite_recipes__user=user)
        return queryset

    class Meta:
        model = Recipes
        fields = ['author', 'tags', 'is_favorited']
