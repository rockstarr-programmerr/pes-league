from django import forms
from django.core.exceptions import ValidationError

from .models import Game, Season, Team, Round
from .logic.game_scheduler import get_schedule
from .utils import is_odd


class GameCreateForm(forms.ModelForm):
    season = forms.ModelChoiceField(Season.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta:
        model = Game
        exclude = ['time']

    def __init__(self, season, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['season'].initial = season
        teams = season.teams.all()
        self.fields['home_team'].queryset = teams
        self.fields['away_team'].queryset = teams

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data['home_team']
        away_team = cleaned_data['away_team']

        if home_team == away_team:
            raise ValidationError('%s tự đá với nhau à?', code='dumb', params=(home_team, ))


class SeasonCreateForm(forms.ModelForm):
    rounds_count = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=38,
        required=True,
        label='Số vòng'
    )

    class Meta:
        model = Season
        fields = ['name', 'rounds_count', 'teams']

    def clean(self):
        cleaned_data = super().clean()
        teams_count = len(cleaned_data['teams'])
        rounds_count = cleaned_data['rounds_count']

        if is_odd(teams_count) and is_odd(rounds_count):
            raise ValidationError(
                ('Nếu số đội lẻ thì số vòng phải chẵn, '
                 'để mỗi đội được đá đủ số trận.'),
                code='invalid'
            )

    def save(self, *args, **kwargs):
        assert kwargs.get('commit', True) is True, \
            '`save` method of `SeasonCreateForm` must be called with commit=True.'

        season = super().save(*args, **kwargs)

        teams = self.cleaned_data['teams']
        rounds_count = self.cleaned_data['rounds_count']

        self._create_rounds(season, rounds_count)
        self._create_games(season, rounds_count, teams)

        return season

    def _create_rounds(self, season, rounds_count):
        rounds = []
        for round_number in range(1, rounds_count + 1):
            rounds.append(
                Round(season=season, number=round_number)
            )

        Round.objects.bulk_create(rounds)

    def _create_games(self, season, rounds_count, teams):
        teams = list(teams)
        schedule = get_schedule(rounds_count, teams)

        rounds = season.rounds.all()
        rounds_map = {}
        for round in rounds:
            key = round.number
            value = round.pk
            rounds_map[key] = value

        games = []
        for index, round in enumerate(schedule):
            round_number = index + 1
            round_pk = rounds_map[round_number]

            for game in round:
                new_game = Game(
                    home_team=game['home'],
                    away_team=game['away'],
                    round_id=round_pk,
                )
                games.append(new_game)

        Game.objects.bulk_create(games)


#######################################
# NOTE: Các form dưới đây chỉ dành cho demo Graphql, hiện tại chưa dùng
#######################################

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = '__all__'

#######################################
