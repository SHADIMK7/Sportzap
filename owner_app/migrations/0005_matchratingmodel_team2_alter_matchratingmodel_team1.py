# Generated by Django 4.2.7 on 2023-11-30 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
        ('owner_app', '0004_remove_matchratingmodel_team2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchratingmodel',
            name='team2',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='team2_match', to='user_app.team'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='matchratingmodel',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1_match', to='user_app.team'),
        ),
    ]
