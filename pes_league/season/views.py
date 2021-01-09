from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView

from .models import Season, Team, Game


class SeasonListView(ListView):
    model = Season
    context_object_name = 'seasons'


class SeasonCreateView(CreateView):
    model = Season
    fields = '__all__'


class SeasonDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        season = get_object_or_404(Season, pk=pk)
        context = {
            'season': season,
        }
        return render(request, 'season/season_detail.html', context)
