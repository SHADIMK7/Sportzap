# Generated by Django 4.2.7 on 2023-11-28 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner_app', '0004_alter_owner_groups_alter_owner_user_permissions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='owner',
            old_name='Phone_number',
            new_name='phone_no',
        ),
    ]
