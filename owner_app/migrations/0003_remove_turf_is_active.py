# Generated by Django 4.2.7 on 2023-12-08 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner_app', '0002_turf_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turf',
            name='is_active',
        ),
    ]