# Generated by Django 4.2.7 on 2023-11-30 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_pic',
            field=models.ImageField(null=True, upload_to='team_image/'),
        ),
    ]
