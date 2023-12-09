from django.db import models
from user_app.models import Team
from owner_app.models import MatchRatingModel
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver





class Leaderboard(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=55) 
    aggregate_score = models.IntegerField(default=0)  
    matches_attended = models.IntegerField(default=0)  
    team_pic = models.ImageField(upload_to='team_image/', null=True)  
    team_strength = models.IntegerField(null=True)  
    number_of_wins = models.IntegerField(default=0)
    win_ratio = models.FloatField(default=0)
    aggregate_score_ratio = models.FloatField(default=0)


     
class Reward(models.Model):
    reward_name = models.CharField(max_length=30)
    reward_image = models.ImageField(upload_to='reward_images/', null=True)
    reward_points = models.IntegerField(default=0)

    def __str__(self):
        return self.reward_name

# TEAM_STATUS = (
#     ('win' , 'win'),
#     ('loss' , 'loss'),
#     ('draw','draw'),
# )

# class TeamPlayer(models.Model):
#     team = models.ForeignKey(Team, related_name='t_team', on_delete=models.SET_NULL, null=True)
#     team_status = models.CharField(choices=TEAM_STATUS, default='draw' ,max_length=30)
#     player = models.JSONField()
#     date = models.DateTimeField()