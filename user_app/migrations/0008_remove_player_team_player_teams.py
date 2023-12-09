# Generated by Django 4.2.7 on 2023-12-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0007_teaminvitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='team',
        ),
        migrations.AddField(
            model_name='player',
            name='teams',
            field=models.ManyToManyField(related_name='players', to='user_app.team'),
        ),
    ]