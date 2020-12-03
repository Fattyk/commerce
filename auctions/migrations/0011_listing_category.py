# Generated by Django 3.1.2 on 2020-12-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20201201_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('FOD', 'FOOD'), ('FAS', 'FASHION'), ('TOY', 'TOYS'), ('ELC', 'ELECTRONICS'), ('HOM', 'HOME'), ('SLR', 'SOLAR'), ('EDU', 'EDUCATION'), ('TEC', 'TECHNOLOGY'), ('PLT', 'PLANTS'), ('ANI', 'ANIMALS')], default='FOD', max_length=3),
        ),
    ]
