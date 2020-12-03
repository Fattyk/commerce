# Generated by Django 3.1.2 on 2020-12-01 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20201201_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='categories',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('FOD', 'FOOD'), ('FAS', 'FASHION'), ('TOY', 'TOYS'), ('ELC', 'ELECTRONICS'), ('HOM', 'HOME'), ('SLR', 'SOLAR'), ('EDU', 'EDUCATION'), ('TEC', 'TECHNOLOGY'), ('PLT', 'PLANTS'), ('ANI', 'ANIMALS')], default='FOD', max_length=3),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
