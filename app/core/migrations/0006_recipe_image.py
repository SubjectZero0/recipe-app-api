# Generated by Django 4.1 on 2022-10-24 17:49

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_ingredient_recipe_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to=core.models.image_path),
        ),
    ]
