# Generated by Django 4.2.7 on 2023-12-01 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner_app', '0003_customer_alter_paymenthistorymodel_user_and_more'),
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
