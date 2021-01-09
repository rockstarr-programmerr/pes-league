from django import forms
from django.core.exceptions import ValidationError

from .models import Game, Season


class GameCreateForm(forms.ModelForm):
    season = forms.ModelChoiceField(Season.objects.all(), required=False, widget=forms.HiddenInput())

    class Meta:
        model = Game
        exclude = ['time']

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data['home_team']
        away_team = cleaned_data['away_team']

        if home_team == away_team:
            raise ValidationError('%s tự đá với nhau à?', code='dumb', params=(home_team, ))
