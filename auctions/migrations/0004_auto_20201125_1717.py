# Generated by Django 3.1.2 on 2020-11-25 16:17

import auctions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201125_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(upload_to=auctions.models.image_directory_path),
        ),
    ]
