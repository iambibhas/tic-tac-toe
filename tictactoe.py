import argparse
import copy
import random


parser = argparse.ArgumentParser()
parser.add_argument("-a", "--against-ai", help="play against AI", action="store_true")
parser.parse_args()


class MoveException(Exception):
    pass


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


def empty_cells(array):
    return [idx for idx, value in enumerate(array) if value == " "]


MINIMAX_SCORE = {"X": 10, "O": -10, "tie": 0}


def minimax(game, depth, is_maximizer):
    if depth == 0 or game.is_winning_move():
        if game.get_winner() is not None:
            return MINIMAX_SCORE[game.winner.symbol]
        else:
            return MINIMAX_SCORE["tie"]

    if is_maximizer:
        best_score = -9999
        for idx in empty_cells(game.game_array):
            game.make_move(idx)
            score = minimax(game, depth - 1, False)
            game.clear_spot(idx)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = 9999
        assert game.current_player == game.players[0]
        for idx in empty_cells(game.game_array):
            game.make_move(idx)
            score = minimax(game, depth - 1, True)
            game.clear_spot(idx)
            best_score = min(score, best_score)
        return best_score


class Player:
    """Player class holding their name and symbol"""

    name: str
    symbol: str
    is_ai: bool

    def __init__(self, name, symbol, is_ai=False):
        self.name = name
        self.symbol = symbol
        self.is_ai = is_ai

    def __str__(self):
        return f"{self.name} [{self.symbol}]"


class Game:
    """Game object to store the state and methods"""

    size: int  # size of the game, e.g. 3 means 3x3 game, 4 means 4x4
    players: list  # list of player objects, arranged by their turn order
    game_array: list  # the game array, a 3x3 game is an array of 9 elements
    winning_patterns: list  # list of winning patterns for the given size
    num_players: int  # number of players
    turn: int  # turn number of the game at any given time
    winner: Player  # winner player

    def __init__(self, size: int = 3, against_ai: bool = False):
        """
        Create the game.

        :param size: size of the game
        :param against_ai: whether the game is against the computer, in which case player 2 is AI
        """
        self.size = size
        self.turn = 1
        self.num_players = 2
        self.players = [
            Player(name="Player 1", symbol="O"),
            Player(name="Player 2", symbol="X", is_ai=against_ai),
        ]

        self.game_array = [" " for i in range(size ** 2)]
        self.winning_patterns = create_winning_patterns(size)
        self.winner = None

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

    def is_winning_move(self) -> bool:
        # check the current game array to see if there is any winning pattern there
        win = False
        for pattern in self.winning_patterns:
            if all(
                [self.game_array[pos] == self.current_player.symbol for pos in pattern]
            ):
                win = True
        return win

    def get_winner(self):
        if self.is_winning_move():
            return self.current_player
        else:
            return None

    def is_end_of_game(self) -> bool:
        # Checks if there is a winning pattern or if all the position has been played
        return self.is_winning_move() or all([pos != " " for pos in self.game_array])

    def best_move(self):
        game_copy = copy.deepcopy(self)
        move: int
        best_score = -9999
        cells = empty_cells(game_copy.game_array)
        for idx in cells:
            end_of_game = game_copy.make_move(idx)
            if end_of_game:
                move = idx
            else:
                score = minimax(game_copy, len(cells), True)
                game_copy.clear_spot(idx)
                print(f"position {idx}, score {score}")
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
                row.append(f"{cell_number}:{self.game_array[cell_number]}   ")
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


def play_game(against_ai: bool = False):
    game = Game(size=3, against_ai=against_ai)

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
            winner = self.get_winner()
            if winner is not None:
                print(f"{winner.name} wins!")
                break
            else:
                print("\nNo winner! Play again.")
                break


if __name__ == "__main__":
    args = parser.parse_args()
    play_game(against_ai=args.against_ai)
