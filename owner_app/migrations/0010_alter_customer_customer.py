# Generated by Django 4.2.7 on 2023-12-01 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owner_app', '0009_alter_customer_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]