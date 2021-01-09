from django import forms

from .models import Game


class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['time']
