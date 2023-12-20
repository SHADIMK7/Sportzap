from user_app.models import Team
from owner_app.models import MatchRatingModel
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from admin_app.models import Leaderboard

@receiver(post_save, sender=MatchRatingModel)
def update_leaderboard(sender, instance, created, **kwargs):

        teams = Team.objects.all()
        for team in teams:
            team_matches = MatchRatingModel.objects.filter(Q(team1=team) | Q(team2=team))

            aggregate_score = sum(
            match.team1_score if match.team1 == team else match.team2_score for match in team_matches
            )
            matches_attended = team_matches.count()
            if matches_attended == 0 :
                 matches_attended = 1

            leaderboard_entry, created = Leaderboard.objects.get_or_create(team=team)
            leaderboard_entry.team_name = team.team_name
            leaderboard_entry.aggregate_score = aggregate_score
            leaderboard_entry.matches_attended = matches_attended
            leaderboard_entry.team_pic = team.team_pic
            leaderboard_entry.team_strength = team.team_strength

            number_of_wins = 0
            for match in team_matches:
                if match.team1_score > match.team2_score:
                    winning_team = match.team1
                else:
                    winning_team = match.team2

                if winning_team == team:
                    number_of_wins += 1

            leaderboard_entry.number_of_wins = number_of_wins
           
            leaderboard_entry.win_ratio = number_of_wins/matches_attended
            leaderboard_entry.aggregate_score_ratio = aggregate_score/matches_attended

            leaderboard_entry.save()
            
            