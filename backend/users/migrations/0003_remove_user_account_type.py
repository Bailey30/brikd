# Generated by Django 5.2.3 on 2025-06-27 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_search_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='account_type',
        ),
    ]
