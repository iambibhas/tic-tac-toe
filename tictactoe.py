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


def get_game_matrix(size: int, game_array: list) -> None:
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            cell_number = i * size + j
            row.append(f"{cell_number}:{game_array[cell_number]}   ")
        matrix.append(row)
    return matrix


def print_game_matrix(size: int, game_array: list) -> None:
    """
    Pretty prints the current game matrix.

    :param size: Size of the game matrix
    :param game_array: The game array holding all player turns
    """
    print("")
    matrix = get_game_matrix(size, game_array)
    for row in matrix:
        print("".join(row))


class Player:
    """Player class holding their name and symbol"""

    name: str
    symbol: str

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class Game:
    """Game object to store the state and methods"""

    size: int  # size of the game, e.g. 3 means 3x3 game, 4 means 4x4
    players: list  # list of player objects, arranged by their turn order
    game_array: list  # the game array, a 3x3 game is an array of 9 elements
    winning_patterns: list  # list of winning patterns for the given size
    num_players: int  # number of players
    turn: int  # turn number of the game at any given time
    winner: Player  # winner player

    def __init__(self, size: int = 3):
        """
        Create the game.

        :param size: size of the game
        """
        self.size = size
        self.turn = 1
        self.num_players = 2
        self.players = [
            Player(name="Player 1", symbol="O"),
            Player(name="Player 2", symbol="X"),
        ]

        self.game_array = [" " for i in range(size ** 2)]
        self.winning_patterns = create_winning_patterns(size)
        self.winner = None

    @property
    def current_player(self) -> Player:
        # player who will play the current turn
        return self.players[(self.turn % len(self.players)) - 1]

    def is_position_taken(self, position: int) -> bool:
        # Check if the given position is taken
        return self.game_array[position] != " "

    def is_winning_move(self) -> bool:
        # check the current game array to see if there is any winning pattern there
        win = False
        for pattern in self.winning_patterns:
            if all(
                [self.game_array[pos] == self.current_player.symbol for pos in pattern]
            ):
                win = True
                self.winner = self.current_player
        return win

    def is_end_of_game(self) -> bool:
        # Checks if there is a winning pattern or if all the position has been played
        return self.is_winning_move() or all([pos != " " for pos in self.game_array])

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

        if self.is_end_of_game():
            return True
        else:
            self.turn += 1
            return False


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


def play_game():
    game = Game(size=3)

    while True:
        print_game_matrix(game.size, game.game_array)

        position = position_input(
            prompt=f"Turn of {game.current_player.name}, enter target position [{game.current_player.symbol}]: ",
            game=game,
        )

        end_of_game = game.make_move(position)

        if end_of_game:
            if game.winner is not None:
                print(f"{game.winner.name} wins!")
            else:
                print("\nNo winner! Play again.")
            break


if __name__ == "__main__":
    # start_game()
    play_game()
