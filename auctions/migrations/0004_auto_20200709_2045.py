# Generated by Django 3.0.8 on 2020-07-09 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200709_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='listing_id',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='listing_id',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='category_id',
            new_name='category',
        ),
    ]
