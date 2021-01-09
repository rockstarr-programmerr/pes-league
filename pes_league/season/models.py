from django.db import models
from django.utils import timezone

# Create your models here.


class Season(models.Model):
    name = models.CharField('Tên', max_length=255)
    length = models.IntegerField('Số trận', default=38)


class Team(models.Model):
    name = models.CharField('Tên', max_length=255)
    manager = models.CharField('Huấn luyện viên', max_length=255)


class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games', verbose_name='Đội nhà')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games', verbose_name='Đội khách')
    home_team_score = models.IntegerField('Số bàn đội nhà')
    away_team_score = models.IntegerField('Số bàn đội khách')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name='Mùa giải')
    date = models.DateField('Ngày thi đấu', default=timezone.now)
