import argparse
import copy
from datetime import datetime
import random
import json
import sqlite3
from typing import Union

con = sqlite3.connect("tictactoe.db")
cur = con.cursor()
# Create the table if it does not exist
with con:
    con.execute(
        "CREATE TABLE IF NOT EXISTS minimax_scores (game_array TEXT, score INTEGER)"
    )
    con.execute("CREATE TABLE IF NOT EXISTS game (created_at INTEGER)")
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS game_move (
            game_id INTEGER,
            player TEXT,
            position INTEGER,
            game_array TEXT,
            FOREIGN KEY (game_id) REFERENCES game(rowid)
        )"""
    )

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--against-ai", help="play against AI", action="store_true")
group = parser.add_mutually_exclusive_group()
group.add_argument("-x", "--server", action="store_true")
group.add_argument("-o", "--client", action="store_true")


class MoveException(Exception):
    pass


def get_score_from_db(game_array: list) -> Union[int, None]:
    cur.execute(
        "SELECT * FROM minimax_scores WHERE game_array=:array",
        {"array": str(game_array)},
    )
    row = cur.fetchone()
    if row is None:
        return None
    else:
        return row[1]


def set_score_in_db(game_array, score) -> None:
    with con:
        con.execute(
            "INSERT INTO minimax_scores (game_array, score) VALUES (:array, :score)",
            {"array": str(game_array), "score": score},
        )


def create_winning_patterns(size: int) -> list:
    """
    Given the size of the game matrix, returns the list of winning patterns.

    :param size: Size of the game matrix
    :returns: List of winning patterns

    >>> create_winning_patterns(2)
    [[0, 1], [0, 2], [2, 3], [1, 3], [0, 3], [1, 2]]
    >>> create_winning_patterns(3)
    [[0, 1, 2], [0, 3, 6], [3, 4, 5], [1, 4, 7], [6, 7, 8], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    """
    patterns = []
    for i in range(size):
        patterns.append([j + i * size for j in range(size)])
        patterns.append([i + j * size for j in range(size)])
    patterns.append([i * size + i for i in range(size)])
    patterns.append([i * (size - 1) + (size - 1) for i in range(size)])
    return patterns


def is_winning_move(size, game_array, symbol) -> bool:
    """
    Check see if there is any winning pattern for the given symbol

    :param size: size of the game, needed to generate winning patterns
    :param game_array: game array containing the state of the game
    :param symbol: symbol to check winning patterns for, e.g. X or O
    """
    win = False
    for pattern in create_winning_patterns(size):
        if all([game_array[pos] == symbol for pos in pattern]):
            win = True
    return win


def get_empty_indices(array: list) -> list:
    return [idx for idx, value in enumerate(array) if value == " "]


def minimax(game_array, players, size, is_maximizer):
    """
    Find the score for the current state of the game array

    Returns a score based on the current player's symbol.
    """
    if is_winning_move(size, game_array, players[0].symbol):
        return players[0].minimax_score
    elif is_winning_move(size, game_array, players[1].symbol):
        return players[1].minimax_score
    elif get_empty_indices(game_array) == []:
        return 0

    if is_maximizer:
        best_score = -9999
        for idx in get_empty_indices(game_array):
            game_array[idx] = players[1].symbol  # Assumed that Player 2 is AI
            # check for the score in the database first
            score = get_score_from_db(game_array)

            if score is None:
                # if not found, minimax it and store it in db
                score = minimax(game_array, players, size, False)
                set_score_in_db(game_array, score)

            game_array[idx] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = 9999
        for idx in get_empty_indices(game_array):
            game_array[idx] = players[0].symbol

            # check for the score in the database first
            score = get_score_from_db(game_array)

            if score is None:
                # if not found, minimax it and store it in db
                score = minimax(game_array, players, size, True)
                set_score_in_db(game_array, score)

            game_array[idx] = " "
            best_score = min(score, best_score)
        return best_score


class Player:
    """Player class holding their name and symbol"""

    symbol: str
    minimax_score: int
    is_ai: bool

    def __init__(self, symbol, minimax_score, is_ai=False):
        self.symbol = symbol
        self.is_ai = is_ai
        self.minimax_score = minimax_score

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f"Player {self.symbol}"


class Game:
    """Game object to store the state and methods"""

    size: int  # size of the game, e.g. 3 means 3x3 game, 4 means 4x4
    players: list  # list of player objects, arranged by their turn order
    game_array: list  # the game array, a 3x3 game is an array of 9 elements
    winning_patterns: list  # list of winning patterns for the given size
    num_players: int  # number of players
    turn: int  # turn number of the game at any given time
    winner: Player  # winner player
    game_id: int
    against_ai: bool

    def __init__(self, game_id: int, against_ai: bool = False):
        """
        Create the game.

        :param size: size of the game
        :param against_ai: whether the game is against the computer, in which case player 2 is AI
        """
        self.against_ai = against_ai
        self.size = 3
        self.game_array = [" " for i in range(size ** 2)]
        self.num_players = 2
        self.players = [
            Player(symbol="X", minimax_score=-1),
            # assuming that player 2 is the AI player in AI mode
            Player(symbol="O", minimax_score=1, is_ai=against_ai),
        ]
        self.winning_patterns = create_winning_patterns(size)
        self.winner = None
        self.turn = 1

        if not against_ai:
            if game_id is None:
                # create game and fetch last move
                cur.execute(
                    "insert into game (created_at) values (:created_at)",
                    {"created_at": datetime.now().timestamp()},
                )
                self.game_id = cur.lastrowid
                self.turn = 1
            else:
                # fetch last move
                cur.execute("select count(*) from game where rowid=:rowid")
                game_obj = cur.fetchone()
                if game_obj is None:
                    raise ValueError("Game ID does not exist")

                self.game_id = game_id

    def get_game_state(self):
        if against_ai:
            return self.game_array
        else:
            cur.execute(
                "select rowid, game_array from game_move where game_id=:game_id order by rowid desc limit 1"
            )
            game_state = cur.fetchone()
            if game_state is None:
                return self.game_array
            else:
                pass

    @property
    def current_player(self) -> Player:
        # player who will play the current turn
        return self.players[(self.turn % self.num_players) - 1]

    def is_position_taken(self, position: int) -> bool:
        array_size = len(self.game_array)
        # Check if the given position is taken
        if position >= array_size:
            raise ValueError(f"Position out of range [0-{array_size - 1}]: {position}")
        return self.game_array[position] != " "

    def get_winner(self) -> Union[Player, None]:
        for player in self.players:
            if is_winning_move(self.size, self.game_array, player.symbol):
                return self.current_player
        else:
            return None

    def is_array_full(self):
        return all([pos != " " for pos in self.game_array])

    def is_end_of_game(self) -> bool:
        # Checks if there is a winning pattern or if all the position has been played
        return (
            is_winning_move(self.size, self.game_array, self.current_player.symbol)
            or self.is_array_full()
        )

    def best_move(self) -> int:
        """
        For the current state of the board, find the best move using minimax()

        Returns the index of game_array for the best move
        """
        game_copy = copy.deepcopy(self)
        move: int = None
        best_score = -9999
        empty_cells = get_empty_indices(game_copy.game_array)
        for idx in empty_cells:
            end_of_game = game_copy.make_move(idx)
            score = minimax(
                game_copy.game_array, game_copy.players, game_copy.size, False
            )
            game_copy.clear_spot(idx)
            if score > best_score:
                best_score = score
                move = idx
        return move

    def clear_spot(self, position: int):
        self.game_array[position] = " "
        self.turn -= 1

    def make_move(self, position: int) -> bool:
        """
        Given a position, place the players symbol in the game array.
        Raises an exception if the given position is taken. The code calling this
        method must handle this exception and send a valid input.

        :param position: position to assign to current player
        :raises MoveExcaption: If the position is taken
        """
        if self.is_position_taken(position):
            raise MoveException("Position already taken")
        self.game_array[position] = self.current_player.symbol

        if not self.is_end_of_game():
            self.turn += 1
            return False
        else:
            return True

    def get_game_matrix(self) -> None:
        matrix = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell_number = i * self.size + j
                row.append(f"{cell_number}: {self.game_array[cell_number]}  |")
            matrix.append(row)
        return matrix

    def print_game_matrix(self) -> None:
        """
        Pretty prints the current game matrix.

        :param size: Size of the game matrix
        :param game_array: The game array holding all player turns
        """
        print("")
        matrix = self.get_game_matrix()
        for row in matrix:
            print("".join(row))
            print("+".join(["------" for _ in range(self.size)]), end="+\n")
        print("")


def position_input(prompt: str, game: Game) -> int:
    """
    Ensures that an integer input within the given range of the game array size is accepted.
    Also checks if the position is taken in the game array, if it is, asks for another position.

    :param prompt: Input prompt to show
    :param array_size: Size of the game matrix
    """
    array_size = len(game.game_array)
    message = f"Invalid position! It must be an integer between 0-{array_size - 1}."
    value = input(prompt)

    # Make sure it's an integer
    try:
        value = int(value)
    except ValueError:
        print(message)
        return position_input(prompt, game)

    # Make sure that it's within the range of the game size
    if 0 <= value < array_size:
        # Make sure that the position is not taken in the game array
        while game.is_position_taken(value):
            value = position_input(
                prompt=f"Position is taken! Enter target position [{game.current_player.symbol}]: ",
                game=game,
            )
        return value
    else:
        print(message)
        return position_input(prompt, game)


def play_against_ai():
    game = Game(size=3, against_ai=True)

    while True:
        game.print_game_matrix()

        if game.current_player.is_ai:
            position = game.best_move()
        else:
            position = position_input(
                prompt=f"Turn of {game.current_player.name}, enter target position [{game.current_player.symbol}]: ",
                game=game,
            )

        print(f"{game.current_player.name} chose position {position}.")
        end_of_game = game.make_move(position)

        if end_of_game:
            game.print_game_matrix()
            winner = game.get_winner()
            if winner is not None:
                print(f"{winner.name} wins!")
                break
            else:
                print("\nNo winner! Play again.")
                break


def play_game():
    pass


if __name__ == "__main__":
    args = parser.parse_args()
    if args.server:
        print("Server mode selected")
    elif args.client:
        print("Client mode selected")
    else:
        print("You need to chose a server or client mode")
    # play_game(against_ai=args.against_ai)
