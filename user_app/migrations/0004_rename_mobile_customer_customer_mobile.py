# Generated by Django 4.2.7 on 2023-11-25 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_rename_customer_phone_number_customer_mobile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='mobile',
            new_name='customer_mobile',
        ),
    ]
