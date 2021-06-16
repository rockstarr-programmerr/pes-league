from django.db.models import IntegerChoices

from .models import Team

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
        self.results = []

    @property
    def gd(self):  # Goal difference
        return self.gf - self.ga

def get_standings(games, season):
    teams = Team.objects.all()
    standings = {
        team.pk: TeamStanding(team)
        for team in teams
    }

    # Theo mặc định, "games" được sắp xếp theo thứ tự trận đấu gần đây nhất lên trước
    # nhưng ở đây cần sắp xếp ngược lại
    # để xử lý logic: Nếu 1 đội bóng đá nhiều hơn số trận tối đa của 1 mùa giải
    # thì những trận từ đó trở đi sẽ không được tính điểm nữa
    games = list(reversed(games))  # Tạo list mới chứ không được mutate list cũ

    for game in games:
        home_team = game.home_team
        away_team = game.away_team

        home_team_won = game.home_team_score > game.away_team_score
        away_team_won = game.away_team_score > game.home_team_score
        draw = not home_team_won and not away_team_won

        # For home team
        home_team_standing = standings[home_team.pk]
        if home_team_standing.games_played < season.length:
            home_team_standing.games_played += 1
            if draw:
                point = 1
                home_team_standing.results.append(Result.DRAW)
            elif home_team_won:
                point = 3
                home_team_standing.results.append(Result.WIN)
            else:
                point = 0
                home_team_standing.results.append(Result.LOSE)

            home_team_standing.points += point
            home_team_standing.gf += game.home_team_score
            home_team_standing.ga += game.away_team_score

        # For away team
        away_team_standing = standings[away_team.pk]
        if away_team_standing.games_played < season.length:
            away_team_standing.games_played += 1
            if draw:
                point = 1
                away_team_standing.results.append(Result.DRAW)
            elif away_team_won:
                point = 3
                away_team_standing.results.append(Result.WIN)
            else:
                point = 0
                away_team_standing.results.append(Result.LOSE)

            away_team_standing.points += point
            away_team_standing.gf += game.away_team_score
            away_team_standing.ga += game.home_team_score

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
