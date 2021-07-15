from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch

from .models import Season, Team, Game
from .forms import GameCreateForm, SeasonCreateForm, GameCreateFormSet
from .logic.team_standing import get_standings, Result


class SeasonListView(ListView):
    model = Season
    context_object_name = 'seasons'


class SeasonCreateView(CreateView):
    model = Season
    form_class = SeasonCreateForm

    @transaction.atomic
    def post(self, *args, **kwargs):
        return super().post(self, *args, **kwargs)


class SeasonDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        season = get_object_or_404(Season, slug=slug)
        if season.is_version_1():
            return self.season_detail_page_version_1(request, season)
        else:
            return self.season_detail_page_version_2(request, season)

    def post(self, request, slug, *args, **kwargs):
        season = get_object_or_404(Season, slug=slug)
        if season.is_version_1():
            return self.save_game_version_1(request, slug, season)
        else:
            return self.save_game_version_2(request, slug, season)

    def season_detail_page_version_2(self, request, season, formset=None):
        round_number = request.GET.get('vong')

        games_qs = Game.objects.all()\
                               .order_by('time')\
                               .select_related('home_team', 'away_team')
        rounds = season.rounds.all().prefetch_related(Prefetch('games', queryset=games_qs))

        current_round = season.get_current_round()

        if not round_number:
            showing_round = current_round
        else:
            showing_round = get_object_or_404(rounds, number=round_number)

        played_games = []
        for round in rounds:
            games = round.games.all()
            played_games.extend(
                game for game in games if game.is_played()
            )

        # Bảng xếp hạng
        standings = get_standings(played_games, season)
        # 5 trận gần nhất
        last_5_games = played_games[-5:]
        last_5_games.reverse()

        # Form tạo trận đấu
        if not formset:
            formset = GameCreateFormSet(
                queryset=showing_round.games.order_by('pk').all(),
                form_kwargs={'season': season}
            )

        context = {
            'season': season,
            'current_round': current_round,
            'showing_round': showing_round,
            'rounds_count': len(rounds),
            'standings': standings,
            'last_5_games': last_5_games,
            'formset': formset,
            'RESULT': Result,
            'time' : range(5)
        }
        return render(request, 'season/season_detail_v2.html', context)

    def save_game_version_2(self, request, slug, season):
        formset = GameCreateFormSet(
            data=request.POST,
            form_kwargs={'season': season}
        )

        if formset.is_valid():
            formset.save()
            messages.success(request, 'Lưu thành công.')
            return redirect('season:season_detail', slug)
        else:
            messages.error(request, 'Lưu thất bại, hãy kiểm tra lại form!')
            return self.season_detail_page_version_2(request, season, formset=formset)

    #############################################################################################
    # Bên dưới là code cho version 1
    #############################################################################################

    def season_detail_page_version_1(self, request, season, form=None):
        all_games = season.get_games().select_related('home_team', 'away_team')
        all_games = list(all_games)  # Evaluate queryset

        # Bảng xếp hạng
        standings = get_standings(all_games, season)
        # 5 trận gần nhất
        last_5_games = all_games[:5]
        # Form tạo trận đấu
        if not form:
            form = GameCreateForm(season=season)

        context = {
            'season': season,
            'standings': standings,
            'last_5_games': last_5_games,
            'form': form,
            'RESULT': Result,
            'time' : range(5)
        }
        return render(request, 'season/season_detail_v1.html', context)

    def save_game_version_1(self, request, slug, season):
        form = GameCreateForm(season=season, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Lưu thành công.')
            return redirect('season:season_detail', slug)
        else:
            messages.error(request, 'Lưu thất bại, hãy kiểm tra lại form!')
            return self.season_detail_page_version_1(request, season, form=form)


class SeasonGameListView(ListView):
    context_object_name = 'games'
    paginate_by = 25

    def get_queryset(self):
        slug = self.request.resolver_match.kwargs['slug']
        season = get_object_or_404(Season, slug=slug)
        games = season.get_played_games()
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
