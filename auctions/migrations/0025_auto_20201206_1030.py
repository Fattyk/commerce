# Generated by Django 3.1.2 on 2020-12-06 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_listing_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploader', to=settings.AUTH_USER_MODEL),
        ),
    ]
