# Generated by Django 2.2.19 on 2023-09-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='is_favorited',
            field=models.BooleanField(default=False, verbose_name='Избранное'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='is_in_shopping_cart',
            field=models.BooleanField(default=False, verbose_name='Список продуктов'),
        ),
    ]
