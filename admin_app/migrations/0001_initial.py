# Generated by Django 4.2.7 on 2023-12-07 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_name', models.CharField(max_length=30)),
                ('reward_image', models.ImageField(null=True, upload_to='reward_images/')),
                ('reward_points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=55)),
                ('aggregate_score', models.IntegerField(default=0)),
                ('matches_attended', models.IntegerField(default=0)),
                ('team_pic', models.ImageField(null=True, upload_to='team_image/')),
                ('team_strength', models.IntegerField(null=True)),
                ('number_of_wins', models.IntegerField(default=0)),
                ('win_ratio', models.FloatField(default=0)),
                ('aggregate_score_ratio', models.FloatField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.team')),
            ],
        ),
    ]