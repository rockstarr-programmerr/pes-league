import random

from django.db.models import IntegerChoices


class Result(IntegerChoices):
    WIN = 1
    DRAW = 2
    LOSE = 3

class TeamStanding:
    def __init__(self, team):
        self.team = team
        self.games_played = 0
        self.points = 0
        self.gf = 0  # Goal forward
        self.ga = 0  # Goal against
        self.win = 0
        self.draw = 0
        self.lose = 0
        self.results = []

    @property
    def gd(self):  # Goal difference
        return self.gf - self.ga

    def _played(self):
        self.games_played += 1

    def won(self, gf, ga):
        self._played()
        self.points += 3
        self.gf += gf
        self.ga += ga
        self.win += 1
        self.results.append(Result.WIN)

    def lost(self, gf, ga):
        self._played()
        self.gf += gf
        self.ga += ga
        self.lose += 1
        self.results.append(Result.LOSE)

    def drew(self, gf, ga):
        self._played()
        self.points += 1
        self.gf += gf
        self.ga += ga
        self.lose += 1
        self.results.append(Result.DRAW)


def get_standings(games, season):
    teams = season.teams.all()
    standings = {
        team.pk: TeamStanding(team)
        for team in teams
    }

    # Theo mặc định, "games" được sắp xếp theo thứ tự trận đấu gần đây nhất lên trước
    # nhưng ở đây cần sắp xếp ngược lại
    # để xử lý logic: Nếu 1 đội bóng đá nhiều hơn số trận tối đa của 1 mùa giải
    # thì những trận từ đó trở đi sẽ không được tính điểm nữa
    # NOTE: Chỉ áp dụng với version 1
    if season.is_version_1():
        games = list(reversed(games))  # Tạo list mới chứ không được mutate list cũ

    for game in games:
        home_team = game.home_team
        away_team = game.away_team

        home_team_won = game.home_team_score > game.away_team_score
        away_team_won = game.away_team_score > game.home_team_score
        draw = not home_team_won and not away_team_won

        # For home team
        home_team_standing = standings[home_team.pk]
        if home_team_standing.games_played < season.get_season_length():
            if draw:
                home_team_standing.drew(game.home_team_score, game.away_team_score)
            elif home_team_won:
                home_team_standing.won(game.home_team_score, game.away_team_score)
            else:
                home_team_standing.lost(game.home_team_score, game.away_team_score)

        # For away team
        away_team_standing = standings[away_team.pk]
        if away_team_standing.games_played < season.get_season_length():
            if draw:
                away_team_standing.drew(game.away_team_score, game.home_team_score)
            elif away_team_won:
                away_team_standing.won(game.away_team_score, game.home_team_score)
            else:
                away_team_standing.lost(game.away_team_score, game.home_team_score)

    standings = list(standings.values())

    # Lấy phong độ 5 trận gần nhất
    for standing in standings:
        standing.results = standing.results[-5:]

    ordering_rule = lambda standing: (
        standing.points,
        standing.gd,
        standing.gf,
        -standing.ga,
    )
    standings.sort(key=ordering_rule, reverse=True)

    return standings
