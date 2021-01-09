from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib import messages

from .models import Season, Team, Game
from .forms import GameCreateForm


class SeasonListView(ListView):
    model = Season
    context_object_name = 'seasons'


class SeasonCreateView(CreateView):
    model = Season
    fields = ['name', 'length']


class SeasonDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        season = get_object_or_404(Season, slug=slug)
        form = GameCreateForm()

        context = {
            'season': season,
            'form': form,
        }

        return render(request, 'season/season_detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        season = get_object_or_404(Season, slug=slug)
        form = GameCreateForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Lưu thành công.')
            return redirect('season:season_detail', slug)

        context = {
            'season': season,
            'form': form,
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


class GameCreateView(View):
    def post(self, request, *args, **kwargs):
        form = GameCreateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('season:season_detail', args=('', ))
