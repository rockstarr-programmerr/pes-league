from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.shortcuts import reverse

# Create your models here.


class Season(models.Model):
    name = models.CharField('tên', max_length=255, unique=True)
    slug = models.SlugField('slug', max_length=255, unique=True)
    length = models.IntegerField('số vòng', default=38)

    class Meta:
        verbose_name = 'mùa giải'
        verbose_name_plural = 'mùa giải'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('season:season_detail', args=(self.slug, ))

    def save(self, *args, **kwargs):
        cleaned_name = self.name.lower().replace('đ', 'd')
        self.slug = slugify(cleaned_name)
        return super().save(*args, **kwargs)


class Team(models.Model):
    name = models.CharField('tên', max_length=255, unique=True)
    slug = models.SlugField('slug', max_length=255, unique=True)
    manager = models.CharField('huấn luyện viên', max_length=255)

    class Meta:
        verbose_name = 'đội bóng'
        verbose_name_plural = 'đội bóng'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('season:team_detail', args=(self.slug, ))

    def save(self, *args, **kwargs):
        cleaned_name = self.name.lower().replace('đ', 'd')
        self.slug = slugify(cleaned_name)
        return super().save(*args, **kwargs)


class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games', verbose_name='đội nhà')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games', verbose_name='đội khách')
    home_team_score = models.IntegerField('bàn thắng đội nhà')
    away_team_score = models.IntegerField('bàn thắng đội khách')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='games', verbose_name='mùa giải')
    time = models.DateTimeField('ngày giờ thi đấu', default=timezone.now)

    class Meta:
        verbose_name = 'trận đấu'
        verbose_name_plural = 'trận đấu'
        ordering = ['-time']

    def __str__(self):
        return f'{self.time.date()}: {self.home_team} {self.home_team_score} - {self.away_team_score} {self.away_team}'

    def get_absolute_url(self):
        return reverse('season:game_detail', args=(self.pk, ))
