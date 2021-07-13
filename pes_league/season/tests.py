from faker import Faker
from model_bakery import baker

from django.test import TestCase
from django.shortcuts import reverse

from .models import Season, Team, Game
from .logic.team_standing import get_standings

fake = Faker()


class StandingTableTwoTeamsTestCase(TestCase):
    def setUp(self):
        self._home_team = Team.objects.create(name='FC gắp bóng', manager='Trung')
        self._away_team = Team.objects.create(name='FC xoạc', manager='Thành LV')
        self._season = Season.objects.create(name='2020-2021', length=38)
        self._season.teams.add(self._home_team, self._away_team)

    def _create_game(self, home_score, away_score):
        return Game.objects.create(
            home_team=self._home_team,
            away_team=self._away_team,
            home_team_score=home_score,
            away_team_score=away_score,
            season=self._season,
        )

    def test_noi_dung_bang_diem__doi_nha_thang(self):
        game = self._create_game(6, 2)
        standings = get_standings([game], self._season)

        home_standing = None
        away_standing = None

        for standing in standings:
            if standing.team.pk == self._home_team.pk:
                home_standing = standing
            elif standing.team.pk == self._away_team.pk:
                away_standing = standing

        self.assertEqual(home_standing.team.name, self._home_team.name)
        self.assertEqual(away_standing.team.name, self._away_team.name)

        self.assertEqual(home_standing.games_played, 1)
        self.assertEqual(home_standing.points, 3)
        self.assertEqual(home_standing.gf, 6)
        self.assertEqual(home_standing.ga, 2)
        self.assertEqual(home_standing.gd, 4)

        self.assertEqual(away_standing.games_played, 1)
        self.assertEqual(away_standing.points, 0)
        self.assertEqual(away_standing.gf, 2)
        self.assertEqual(away_standing.ga, 6)
        self.assertEqual(away_standing.gd, -4)

    def test_noi_dung_bang_diem__doi_khach_thang(self):
        game = self._create_game(4, 11)
        standings = get_standings([game], self._season)

        home_standing = None
        away_standing = None

        for standing in standings:
            if standing.team.pk == self._home_team.pk:
                home_standing = standing
            elif standing.team.pk == self._away_team.pk:
                away_standing = standing

        self.assertEqual(home_standing.team.name, self._home_team.name)
        self.assertEqual(away_standing.team.name, self._away_team.name)

        self.assertEqual(home_standing.games_played, 1)
        self.assertEqual(home_standing.points, 0)
        self.assertEqual(home_standing.gf, 4)
        self.assertEqual(home_standing.ga, 11)
        self.assertEqual(home_standing.gd, -7)

        self.assertEqual(away_standing.games_played, 1)
        self.assertEqual(away_standing.points, 3)
        self.assertEqual(away_standing.gf, 11)
        self.assertEqual(away_standing.ga, 4)
        self.assertEqual(away_standing.gd, 7)

    def test_noi_dung_bang_diem__hoa(self):
        game = self._create_game(0, 0)
        standings = get_standings([game], self._season)

        home_standing = None
        away_standing = None

        for standing in standings:
            if standing.team.pk == self._home_team.pk:
                home_standing = standing
            elif standing.team.pk == self._away_team.pk:
                away_standing = standing

        self.assertEqual(home_standing.team.name, self._home_team.name)
        self.assertEqual(away_standing.team.name, self._away_team.name)

        self.assertEqual(home_standing.games_played, 1)
        self.assertEqual(home_standing.points, 1)
        self.assertEqual(home_standing.gf, 0)
        self.assertEqual(home_standing.ga, 0)
        self.assertEqual(home_standing.gd, 0)

        self.assertEqual(away_standing.games_played, 1)
        self.assertEqual(away_standing.points, 1)
        self.assertEqual(away_standing.gf, 0)
        self.assertEqual(away_standing.ga, 0)
        self.assertEqual(away_standing.gd, 0)

    def test_noi_dung_bang_diem__nhieu_tran(self):
        standings = get_standings([
            self._create_game(3, 1),
            self._create_game(4, 0),
            self._create_game(5, 4),
            self._create_game(2, 2),
            self._create_game(0, 1),
            self._create_game(1, 4),
            self._create_game(0, 0),
        ], self._season)

        home_standing = None
        away_standing = None

        for standing in standings:
            if standing.team.pk == self._home_team.pk:
                home_standing = standing
            elif standing.team.pk == self._away_team.pk:
                away_standing = standing

        self.assertEqual(home_standing.team.name, self._home_team.name)
        self.assertEqual(away_standing.team.name, self._away_team.name)

        self.assertEqual(home_standing.games_played, 7)
        self.assertEqual(home_standing.points, 11)
        self.assertEqual(home_standing.gf, 15)
        self.assertEqual(home_standing.ga, 12)
        self.assertEqual(home_standing.gd, 3)

        self.assertEqual(away_standing.games_played, 7)
        self.assertEqual(away_standing.points, 8)
        self.assertEqual(away_standing.gf, 12)
        self.assertEqual(away_standing.ga, 15)
        self.assertEqual(away_standing.gd, -3)

    def test_xep_hang__khac_diem__doi_nha_thang(self):
        standings = get_standings([
            self._create_game(1, 0),
            self._create_game(4, 0),
            self._create_game(2, 2),
            self._create_game(3, 2),
        ], self._season)

        first_place = standings[0]
        second_place = standings[1]

        self.assertNotEqual(first_place.points, second_place.points)
        self.assertEqual(first_place.team.name, self._home_team.name)
        self.assertEqual(second_place.team.name, self._away_team.name)

    def test_xep_hang__khac_diem__doi_khach_thang(self):
        standings = get_standings([
            self._create_game(1, 0),
            self._create_game(4, 5),
            self._create_game(2, 3),
            self._create_game(3, 3),
        ], self._season)

        first_place = standings[0]
        second_place = standings[1]

        self.assertNotEqual(first_place.points, second_place.points)
        self.assertEqual(first_place.team.name, self._away_team.name)
        self.assertEqual(second_place.team.name, self._home_team.name)

    def test_xep_hang__bang_diem__khac_hieu_so__doi_nha_thang(self):
        standings = get_standings([
            self._create_game(3, 0),
            self._create_game(4, 2),
            self._create_game(0, 1),
            self._create_game(0, 2),
        ], self._season)

        first_place = standings[0]
        second_place = standings[1]

        self.assertEqual(first_place.points, second_place.points)
        self.assertNotEqual(first_place.gd, second_place.gd)
        self.assertEqual(first_place.team.name, self._home_team.name)
        self.assertEqual(second_place.team.name, self._away_team.name)

    def test_xep_hang__bang_diem__khac_hieu_so__doi_khach_thang(self):
        standings = get_standings([
            self._create_game(1, 0),
            self._create_game(1, 0),
            self._create_game(2, 2),
            self._create_game(2, 1),
            self._create_game(2, 3),
            self._create_game(0, 3),
            self._create_game(2, 5),
        ], self._season)

        first_place = standings[0]
        second_place = standings[1]

        self.assertEqual(first_place.points, second_place.points)
        self.assertNotEqual(first_place.gd, second_place.gd)
        self.assertEqual(first_place.team.name, self._away_team.name)
        self.assertEqual(second_place.team.name, self._home_team.name)

    # Không test được trường hợp bằng điểm, bằng hiệu số, khác bàn thắng
    # khi chỉ có 2 team đá với nhau
    # Vì khi đó bàn thắng của team này là bàn thua của team kia
    # 2 team bằng hiệu số chỉ khi cả 2 ghi bàn bằng nhau và hiệu số bằng đúng 0


class StandingTableThreeTeamsTestCase(TestCase):
    def setUp(self):
        self._team_1 = Team.objects.create(name='FC tấu hài', manager='Tuấn LA')
        self._team_2 = Team.objects.create(name='FC hihi haha', manager='Tuấn DV')
        self._team_3 = Team.objects.create(name='FC gắp bóng', manager='Trung')
        self._team_4 = Team.objects.create(name='FC xoạc', manager='Thành LV')
        self._season = Season.objects.create(name='Fun league')
        self._season.teams.add(self._team_1, self._team_2, self._team_3, self._team_4)

    def _create_game(self, home_team, away_team, home_team_score, away_team_score):
        return Game.objects.create(
            home_team=home_team,
            away_team=away_team,
            home_team_score=home_team_score,
            away_team_score=away_team_score,
            season=self._season,
        )

    def test_xep_hang__bang_diem__bang_hieu_so__khac_ban_thang__team_1_thang(self):
        standings = get_standings([
            self._create_game(self._team_1, self._team_2, 3, 1),
            self._create_game(self._team_1, self._team_2, 5, 4),
            self._create_game(self._team_2, self._team_1, 3, 1),
            self._create_game(self._team_2, self._team_1, 1, 0),
            self._create_game(self._team_1, self._team_3, 4, 3),
            self._create_game(self._team_2, self._team_3, 1, 0),
            self._create_game(self._team_3, self._team_4, 1, 0),
        ],self._season)

        first_place = standings[0]
        second_place = standings[1]
        third_place = standings[2]
        forth_place = standings[3]

        self.assertEqual(first_place.points, second_place.points)
        self.assertEqual(first_place.gd, second_place.gd)
        self.assertNotEqual(first_place.gf, second_place.gf)

        self.assertEqual(first_place.team.name, self._team_1.name)
        self.assertEqual(second_place.team.name, self._team_2.name)
        self.assertEqual(third_place.team.name, self._team_3.name)
        self.assertEqual(forth_place.team.name, self._team_4.name)

    def test_xep_hang__bang_diem__bang_hieu_so__khac_ban_thang__team_2_thang(self):
        standings = get_standings([
            self._create_game(self._team_1, self._team_2, 3, 1),
            self._create_game(self._team_1, self._team_2, 5, 4),
            self._create_game(self._team_1, self._team_2, 1, 1),
            self._create_game(self._team_2, self._team_1, 3, 1),
            self._create_game(self._team_2, self._team_1, 5, 4),
            self._create_game(self._team_1, self._team_3, 1, 3),
            self._create_game(self._team_2, self._team_3, 2, 4),
            self._create_game(self._team_3, self._team_4, 0, 1),
            self._create_game(self._team_3, self._team_4, 0, 4),
        ],self._season)

        first_place = standings[0]
        second_place = standings[1]
        third_place = standings[2]
        forth_place = standings[3]

        self.assertEqual(first_place.points, second_place.points)
        self.assertEqual(first_place.gd, second_place.gd)
        self.assertNotEqual(first_place.gf, second_place.gf)

        self.assertEqual(first_place.team.name, self._team_2.name)
        self.assertEqual(second_place.team.name, self._team_1.name)
        self.assertEqual(third_place.team.name, self._team_4.name)
        self.assertEqual(forth_place.team.name, self._team_3.name)

    def test_da_qua_so_tran_cua_mua_giai(self):
        games = []

        # Đội 1 và 2 đá đủ 38 trận
        for i in range(38):
            game = self._create_game(self._team_1, self._team_2, 1, 1)
            games.append(game)

        # Đội 3 và 4 mới đá 37 trận
        for i in range(37):
            game = self._create_game(self._team_3, self._team_4, 2, 2)
            games.append(game)

        # Assert
        standings = get_standings(games, self._season)

        standing_team_1 = None
        standing_team_2 = None
        standing_team_3 = None
        standing_team_4 = None

        for standing in standings:
            if standing.team.pk == self._team_1.pk:
                standing_team_1 = standing
            elif standing.team.pk == self._team_2.pk:
                standing_team_2 = standing
            elif standing.team.pk == self._team_3.pk:
                standing_team_3 = standing
            elif standing.team.pk == self._team_4.pk:
                standing_team_4 = standing

        self.assertEqual(standing_team_1.points, 38)
        self.assertEqual(standing_team_2.points, 38)
        self.assertEqual(standing_team_3.points, 37)
        self.assertEqual(standing_team_4.points, 37)

        # Đội 1 vs đội 4 => Chỉ đội 4 được tính điểm
        game = self._create_game(self._team_1, self._team_4, 1, 1)
        games.append(game)
        # Đội 2 vs đội 3 => Chỉ đội 3 được tính điểm
        game = self._create_game(self._team_2, self._team_3, 0, 0)
        games.append(game)

        # Assert
        standings = get_standings(games, self._season)

        standing_team_1 = None
        standing_team_2 = None
        standing_team_3 = None
        standing_team_4 = None

        for standing in standings:
            if standing.team.pk == self._team_1.pk:
                standing_team_1 = standing
            elif standing.team.pk == self._team_2.pk:
                standing_team_2 = standing
            elif standing.team.pk == self._team_3.pk:
                standing_team_3 = standing
            elif standing.team.pk == self._team_4.pk:
                standing_team_4 = standing

        self.assertEqual(standing_team_1.points, 38)
        self.assertEqual(standing_team_2.points, 38)
        self.assertEqual(standing_team_3.points, 38)
        self.assertEqual(standing_team_4.points, 38)


class SeasonCreateTestCase(TestCase):
    def create_season_and_teams(self, teams_count, rounds_count):
        url = reverse('season:season_create')
        self.teams = baker.make(Team, _quantity=teams_count)
        season_name = fake.text(max_nb_chars=30)
        self.client.post(url, {
            'name': season_name,
            'rounds_count': rounds_count,
            'teams': [team.pk for team in self.teams],
        })
        self.season = Season.objects.filter(name=season_name).prefetch_related('rounds__games').first()
        self.assertIsNotNone(self.season)

    def test_rounds_created_auto_magically_after_creating_season(self):
        self.create_season_and_teams(3, 38)
        rounds = self.season.rounds.all()
        for index, round in enumerate(rounds):
            self.assertEqual(round.season_id, self.season.pk)
            self.assertEqual(round.number, index + 1)

    def test_games_created_auto_magically_after_creating_season(self):
        # Even teams
        self.create_season_and_teams(20, 38)
        games = self.season.get_games()
        self.assertEqual(len(games), 380)

        self.create_season_and_teams(4, 6)
        games = self.season.get_games()
        self.assertEqual(len(games), 12)

        # Odd teams
        self.create_season_and_teams(7, 42)
        games = self.season.get_games()
        self.assertEqual(len(games), 126)

        self.create_season_and_teams(7, 21)
        games = self.season.get_games()
        self.assertEqual(len(games), 63)
