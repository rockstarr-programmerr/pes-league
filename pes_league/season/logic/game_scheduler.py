import random
from ..utils import is_odd


def get_schedule(rounds_count, teams):
    """
    Input:
        `rounds_count` (int): số vòng
        `teams` (list): danh sách các đội

    Return format:
    [  <-- All rounds
        [  <-- Each round
            {"home": ..., "away": ...},
            {"home": ..., "away": ...},
            .etc
        ],
        .etc
    ]

    Mô tả thuật toán:
        Giả sử có 8 đội: A, B, C, D, E, F, G, H

        Bước 1: Xếp 8 đội thành 2 nhóm:
            Nhóm 1: A, B, C, D
            Nhóm 2: E, F, G, H
        Bước 2: Ghép từng vị trí của nhóm 1 với nhóm 2, được một vòng:
            A-E, B-F, C-G, D-H
        Bước 3: Giữ nguyên đội A, tất cả các đội còn lại dịch chuyển sang phải 1 vị trí:
            Nhóm 1: A, E, B, C
            Nhóm 2: F, G, H, D
        Bước 4: Lặp lại từ bước 2 đến khi nào hết số vòng.

        Nếu số đội lẻ, thêm 1 đội bù nhìn vào cho thành chẵn.
        Thực hiện thuật toán như bình thường.
        Với mỗi vòng, đội nào được ghép cặp với đội bù nhìn thì không cần đá.
    """
    _add_dummy_team_if_needed(teams)
    _randomize_teams_order(teams)
    first_group, second_group = _split_teams_to_two_groups(teams)

    schedule = []
    while rounds_count > 0:
        # Đảo đội nhà, đội khách giữa mỗi vòng
        if is_odd(rounds_count):
            games = _create_games(first_group, second_group)
        else:
            games = _create_games(second_group, first_group)

        schedule.append(games)

        _rotate_teams(first_group, second_group)
        rounds_count -= 1

    _remove_dummy_games(schedule)

    return schedule


class _DummyTeam:
    pass

def _is_dummy_team(team):
    return isinstance(team, _DummyTeam)

def _add_dummy_team_if_needed(teams):
    if is_odd(len(teams)):
        teams.append(_DummyTeam())

def _randomize_teams_order(teams):
    random.shuffle(teams)

def _split_teams_to_two_groups(teams):
    half = int(len(teams) / 2)
    first_group = teams[:half]
    second_group = teams[half:]
    return first_group, second_group

def _create_games(home_teams, away_teams):
    games_count = len(home_teams)  # `home_teams` và `away_teams` có cùng số đội
    games = []
    for i in range(games_count):
        home_team = home_teams[i]
        away_team = away_teams[i]
        games.append({
            'home': home_team,
            'away': away_team,
        })
    return games

def _rotate_teams(first_group, second_group):
    """
    >>> first_group = [1, 2, 3, 4]
    >>> second_group = [1, 2, 3, 4]
    >>> _rotate_teams(first_group, second_group)
    >>> first_group
    [1, 5, 2, 3]
    >>> second_group
    [6, 7, 8, 4]
    """
    last_team_of_first_group = first_group.pop()
    second_group.append(last_team_of_first_group)

    first_team_of_second_group = second_group.pop(0)
    first_group.insert(1, first_team_of_second_group)

def _remove_dummy_games(schedule):
    for round in schedule:
        dummy_game_indexes = []

        for index, game in enumerate(round):
            home_team = game['home']
            away_team = game['away']
            if _is_dummy_team(home_team) or _is_dummy_team(away_team):
                dummy_game_indexes.append(index)

        dummy_game_indexes.reverse()  # Muốn xóa các phần tử của list bằng index thì phải xóa từ index lớn nhất trước
        for index in dummy_game_indexes:
            round.pop(index)
