# Generated by Django 3.0.8 on 2020-07-13 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200713_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='posted',
            field=models.DateTimeField(auto_now=True),
        ),
    ]