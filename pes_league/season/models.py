from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.shortcuts import reverse

# Create your models here.


class Season(models.Model):
    name = models.CharField('Tên', max_length=255, unique=True)
    slug = models.SlugField('slug', max_length=255, unique=True)
    length = models.IntegerField('Số vòng', default=38)

    def __str__(self):
        return f'{self.id} - {self.name}'

    def get_absolute_url(self):
        return reverse('season:season_detail', args=(self.slug, ))

    def save(self, *args, **kwargs):
        cleaned_name = self.name.lower().replace('đ', 'd')
        self.slug = slugify(cleaned_name)
        return super().save(*args, **kwargs)


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
