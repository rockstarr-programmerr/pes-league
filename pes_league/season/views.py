from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView

from .models import Season, Team, Game


class SeasonListView(ListView):
    model = Season
    context_object_name = 'seasons'


class SeasonCreateView(CreateView):
    model = Season
    fields = ['name', 'length']


class SeasonDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        season = get_object_or_404(Season, slug=slug)
        context = {
            'season': season,
        }
        return render(request, 'season/season_detail.html', context)


class TeamListView(ListView):
    model = Team
    context_object_name = 'teams'


class TeamCreateView(CreateView):
    model = Team
    fields = ['name', 'manager']


class TeamDetailView(DetailView):
    model = Team
