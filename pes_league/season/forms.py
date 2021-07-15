from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Game, Season, Team, Round
from .logic.game_scheduler import get_schedule
from .utils import is_odd


class GameCreateForm(forms.ModelForm):
    season = forms.ModelChoiceField(Season.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta:
        model = Game
        exclude = ['time', 'round']

    def __init__(self, season=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'season' in self.fields:
            self.fields['season'].initial = season

        teams = season.teams.all()
        self.fields['home_team'].queryset = teams
        self.fields['away_team'].queryset = teams

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        instance = super().save(*args, **kwargs)
        instance.time = timezone.now()
        self.save_m2m()
        return instance.save()

    def clean(self):
        cleaned_data = super().clean()
        self._validate_team(cleaned_data)
        self._validate_score(cleaned_data)

    def _validate_team(self, cleaned_data):
        home_team = cleaned_data['home_team']
        away_team = cleaned_data['away_team']

        if home_team == away_team:
            raise ValidationError('%s tự đá với nhau à?', code='dumb', params=(home_team.name, ))

    def _validate_score(self, cleaned_data):
        home_team_score = cleaned_data['home_team_score']
        away_team_score = cleaned_data['away_team_score']

        if (
            (home_team_score is not None and away_team_score is None) or
            (away_team_score is not None and home_team_score is None)
        ):
            raise ValidationError('Chưa nhập đủ thông tin.', code='dumb')


class GameCreateFormV2(GameCreateForm):
    round = forms.ModelChoiceField(Round.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta(GameCreateForm.Meta):
        exclude = ['time', 'season']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['home_team'].disabled = True
        self.fields['away_team'].disabled = True

        game = self.instance
        if game.is_played():
            self.fields['home_team_score'].disabled = True
            self.fields['away_team_score'].disabled = True


GameCreateFormSet = forms.modelformset_factory(Game, form=GameCreateFormV2, extra=0, can_delete=False)


class SeasonCreateForm(forms.ModelForm):
    turns_count = forms.IntegerField(
        min_value=1,
        max_value=50,
        required=True,
        label='Số lượt trận',
    )
    rounds_count = forms.IntegerField(
        min_value=1,
        required=True,
        label='Số vòng',
        help_text='Số vòng được tự tính theo số đội và số lượt trận.',
        widget=forms.NumberInput(attrs={'readonly': True}),
    )

    class Meta:
        model = Season
        fields = ['name', 'teams', 'turns_count']
        help_texts = {
            'teams': 'Giữ shift để chọn nhiều đội.',
        }

    def save(self, *args, **kwargs):
        assert kwargs.get('commit', True) is True, \
            '`save` method of `SeasonCreateForm` must be called with commit=True.'

        season = super().save(*args, **kwargs)

        teams = self.cleaned_data['teams']
        turns_count = self.cleaned_data['turns_count']

        teams_count = len(teams)
        if is_odd(teams_count):
            rounds_count = teams_count * turns_count
        else:
            rounds_count = (teams_count - 1) * turns_count

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
                    time=None,  # Trận chưa đá nên time = None
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
