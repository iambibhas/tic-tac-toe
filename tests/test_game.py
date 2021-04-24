from tictactoe import (
    Player,
    Game,
    create_winning_patterns,
    get_game_matrix,
    print_game_matrix,
)


def test_create_winning_patterns():
    assert create_winning_patterns(2) == [
        [0, 1],
        [0, 2],
        [2, 3],
        [1, 3],
        [0, 3],
        [1, 2],
    ]
    assert create_winning_patterns(3) == [
        [0, 1, 2],
        [0, 3, 6],
        [3, 4, 5],
        [1, 4, 7],
        [6, 7, 8],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    assert create_winning_patterns(6) == [
        [0, 1, 2, 3, 4, 5],
        [0, 6, 12, 18, 24, 30],
        [6, 7, 8, 9, 10, 11],
        [1, 7, 13, 19, 25, 31],
        [12, 13, 14, 15, 16, 17],
        [2, 8, 14, 20, 26, 32],
        [18, 19, 20, 21, 22, 23],
        [3, 9, 15, 21, 27, 33],
        [24, 25, 26, 27, 28, 29],
        [4, 10, 16, 22, 28, 34],
        [30, 31, 32, 33, 34, 35],
        [5, 11, 17, 23, 29, 35],
        [0, 7, 14, 21, 28, 35],
        [5, 10, 15, 20, 25, 30],
    ]
