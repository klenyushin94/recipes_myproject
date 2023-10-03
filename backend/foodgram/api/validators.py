from rest_framework import serializers


class RecipesCreateUpdateValidator:
    def __call__(self, data):
        ingredients = data.get('ingredients', [])
        cooking_time = data.get('cooking_time')

        if cooking_time is not None and cooking_time < 0:
            raise serializers.ValidationError(
                "Ошибка! Время приготовления не может быть отрицательным"
            )

        if len(ingredients) == 0:
            raise serializers.ValidationError(
                "Ошибка! Должен быть хотя бы один игредиент"
            )

        ingredient_ids = set()
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            amount = ingredient.get('amount')

            if amount is not None and amount < 0:
                raise serializers.ValidationError(
                    "Ошибка! Количество ингредиента не может быть "
                    "отрицательным"
                )

            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    "Один из ингредиентов добавлен несколько раз"
                )
            ingredient_ids.add(ingredient_id)
