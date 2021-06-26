from django import forms
from django.core.exceptions import ValidationError

from .models import Game, Season, Team


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


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = '__all__'
