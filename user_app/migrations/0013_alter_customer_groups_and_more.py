# Generated by Django 4.2.7 on 2023-11-29 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user_app', '0012_delete_turfbooking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='groups',
            field=models.ManyToManyField(null=True, related_name='customer_groups', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user_permissions',
            field=models.ManyToManyField(null=True, related_name='customer_user_permissions', to='auth.permission'),
        ),
    ]
