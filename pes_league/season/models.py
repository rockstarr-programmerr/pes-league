from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.shortcuts import reverse


class Team(models.Model):
    name = models.CharField('tên', max_length=255, unique=True)
    slug = models.SlugField('slug', max_length=255, unique=True, blank=True)
    manager = models.CharField('huấn luyện viên', max_length=255)

    class Meta:
        verbose_name = 'đội bóng'
        verbose_name_plural = 'đội bóng'

    def __str__(self):
        return f'{self.name} ({self.manager})'

    def get_absolute_url(self):
        return reverse('season:team_detail', args=(self.slug, ))

    def save(self, *args, **kwargs):
        cleaned_name = self.name.lower().replace('đ', 'd')
        self.slug = slugify(cleaned_name)
        return super().save(*args, **kwargs)


class Season(models.Model):
    name = models.CharField('tên', max_length=255, unique=True)
    slug = models.SlugField('slug', max_length=255, unique=True, blank=True)
    length = models.PositiveSmallIntegerField('số vòng', blank=True, null=True)
    teams = models.ManyToManyField(Team, related_name='seasons', verbose_name='đội bóng')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'mùa giải'
        verbose_name_plural = 'mùa giải'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('season:season_detail', args=(self.slug, ))

    def save(self, *args, **kwargs):
        cleaned_name = self.name.lower().replace('đ', 'd')
        self.slug = slugify(cleaned_name)
        return super().save(*args, **kwargs)

    def is_version_1(self):
        """Mùa giải này có phải được tạo từ version 1 hay không?

        Từ version 2, có thêm tính năng sắp xếp vòng đấu (thêm bảng `Round`).
        Không cần lưu `length` nữa, vì số vòng có thể tính được từ số `Round` foreignkey đến `Season`.
        => Nếu `Season` có `length` = NULL thì là version 2, còn lại là version 1.

        NOTE: Không được xóa hẳn cột `length` đi vì nếu xóa, các mùa giải tạo từ version 1 sẽ mất dữ liệu.
        """
        return self.length is None

    def get_games(self):
        games = []
        rounds = self.rounds.all()
        for round_ in rounds:
            games.extend(round_.games.all())
        return games


class Round(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='rounds', verbose_name='vòng đấu')
    number = models.PositiveSmallIntegerField('vòng số')

    class Meta:
        verbose_name = 'vòng đấu'
        verbose_name_plural = 'vòng đấu'
        ordering = ['number']

    def __str__(self):
        return f'Vòng số {self.number}'


class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games', verbose_name='đội nhà')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games', verbose_name='đội khách')
    home_team_score = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='bàn thắng đội nhà')
    away_team_score = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='bàn thắng đội khách')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, related_name='games', verbose_name='mùa giải')
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=True, related_name='games', verbose_name='vòng đấu')
    time = models.DateTimeField('ngày giờ thi đấu', default=timezone.now)

    class Meta:
        verbose_name = 'trận đấu'
        verbose_name_plural = 'trận đấu'
        ordering = ['-time']

    def __str__(self):
        return f'{self.time.date()}: {self.home_team} {self.home_team_score} - {self.away_team_score} {self.away_team}'

    def get_absolute_url(self):
        return reverse('season:game_detail', args=(self.pk, ))

    def is_played(self):
        return self.home_team_score is not None and self.away_team_score is not None

    def is_version_1(self):
        """Trận đấu này có phải được tạo từ version 1 hay không?

        Từ version 2, có thêm tính năng sắp xếp vòng đấu (thêm bảng `Round`).
        Khi lưu `Game`, sẽ lưu luôn game đó thuộc `Round` nào.
        => `Game` nào mà `round` = NULL thì là version 1, còn lại là version 2.

        NOTE: Không được xóa hẳn cột `season` đi vì nếu xóa, các trận đấu tạo từ version 1 sẽ mất dữ liệu.
        Nhưng từ version 2, khi tạo `Game` thì sẽ chỉ lưu `round`, không lưu `season` nữa.
        """
        return self.round is None
