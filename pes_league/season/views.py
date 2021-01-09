from django.shortcuts import render

from .models import Season, Team, Game


def season_list(request):
    seasons = Season.objects.all()
    return render(request, 'season/season_list.html', {'seasons': seasons})
