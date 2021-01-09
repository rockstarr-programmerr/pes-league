import copy

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib import messages

from .models import Season, Team, Game
from .forms import GameCreateForm
from .logic import get_standings


class SeasonListView(ListView):
    model = Season
    context_object_name = 'seasons'


class SeasonCreateView(CreateView):
    model = Season
    fields = ['name', 'length']


class SeasonDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        season = get_object_or_404(Season, slug=slug)
        all_games = season.games.all().select_related('home_team', 'away_team')

        # Bảng xếp hạng
        standings = get_standings(all_games, season)

        # 5 trận gần nhất
        games = all_games[:5]

        # Form tạo trận đấu
        form = GameCreateForm()

        context = {
            'season': season,
            'standings': standings,
            'games': games,
            'form': form,
        }

        return render(request, 'season/season_detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        season = get_object_or_404(Season, slug=slug)

        data = copy.deepcopy(request.POST)
        data['season'] = season
        form = GameCreateForm(data)

        if form.is_valid():
            form.save()
            messages.success(request, 'Lưu thành công.')
            return redirect('season:season_detail', slug)

        else:
            messages.error(request, 'Lưu thất bại, hãy kiểm tra lại form!')
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


class GameListView(ListView):
    model = Game
    context_object_name = 'games'


class GameDetailView(DetailView):
    model = Game
