# Generated by Django 3.1.2 on 2020-12-01 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201130_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watch',
            old_name='watchlist',
            new_name='listing',
        ),
    ]
