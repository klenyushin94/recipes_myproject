# Generated by Django 2.2.19 on 2023-09-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230912_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_subscribed',
            field=models.BooleanField(default=False, verbose_name='Подписка'),
        ),
    ]
