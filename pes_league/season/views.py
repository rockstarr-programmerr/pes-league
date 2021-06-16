import copy

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib import messages

from .models import Season, Team, Game
from .forms import GameCreateForm
from .logic import get_standings, Result


class SeasonListView(ListView):
    model = Season
    context_object_name = 'seasons'


class SeasonCreateView(CreateView):
    model = Season
    fields = ['name', 'length', 'teams']


class SeasonDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        season = get_object_or_404(Season, slug=slug)
        all_games = season.games.all().select_related('home_team', 'away_team')
        all_games = list(all_games)  # Evaluate queryset

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
            'RESULT': Result,
            'time' : range(5)
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


class SeasonGameListView(ListView):
    context_object_name = 'games'
    paginate_by = 25

    def get_queryset(self):
        slug = self.request.resolver_match.kwargs['slug']
        season = get_object_or_404(Season, slug=slug)
        games = season.games.all()
        return games


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
    paginate_by = 25


class GameDetailView(DetailView):
    model = Game
