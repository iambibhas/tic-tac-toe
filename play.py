from dataclasses import dataclass


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
        patterns.append([j+i*size for j in range(size)])
        patterns.append([i+j*size for j in range(size)])
    patterns.append([i*size+i for i in range(size)])
    patterns.append([i*(size-1)+(size-1) for i in range(size)])
    return patterns


def print_game_matrix(size: int, array: list) -> None:
    """
    Pretty prints the current game matrix.

    :param size: Size of the game matrix
    :param array: The game array holding all player turns
    """
    print("\n")
    for i in range(size*size):
        print(f"{i}:{array[i]}   ", end="")
        if (i + 1) % size == 0:
            print("\n")


def position_input(prompt: str, array_size: int) -> int:
    """
    Ensures that an integer input within the given range of the game array size is accepted.

    :param prompt: Input prompt to show
    :param array_size: Size of the game matrix
    """
    message = f"Invalid position! It must be an integer between 0-{array_size - 1}."
    value = input(prompt)
    try:
        value = int(value)
    except ValueError:
        print(message)
        return position_input(prompt, array_size)
    if 0 <= value < array_size:
        return value
    else:
        print(message)
        return position_input(prompt, array_size)


@dataclass
class Player:
    """Player class holding their name and symbol"""
    name: str
    symbol: str


def start_game():
    # Name and order of the players are preset for now
    player1 = Player(name="Player 1", symbol="O")
    player2 = Player(name="Player 2", symbol="X")
    players = [player1, player2]

    # Size of the game matrix, preset for now
    size = 3
    # An array, where all items are ` ` to start with
    game_array = [" " for i in range(size*size)]
    # Fetch all the winning patterns. We'll compare this at the end of the turn.
    winning_patterns = create_winning_patterns(size)

    turn = 0
    while True:
        turn += 1
        current_player = players[turn % len(players) - 1]

        print_game_matrix(size, game_array)

        position = position_input(f"Turn of {current_player.name}, enter target position [{current_player.symbol}]: ", len(game_array))

        # Check if the position is taken already
        if game_array[position] != " ":
            while game_array[position] != " ":
                position = position_input(f"Position already taken! Enter target position [{current_player.symbol}]: ", len(game_array))

        print(f"\n{current_player.name} placed {current_player.symbol} in position {position}.")
        game_array[position] = current_player.symbol

        if turn >= size + (size - 1):
            # it'll take at least `size + (size - 1)` turns for the starting user to
            # reach a winning patterns if not blocked by the other user
            win = False
            for pattern in winning_patterns:
                if all([game_array[pos] == current_player.symbol for pos in pattern]):
                    win = True

            if win:
                print_game_matrix(size, game_array)
                print(f"{current_player.name} wins!")
                break

            if all([pos != " " for pos in game_array]):
                print("\nNo winner! Play again.")
                break

if __name__ == "__main__":
    start_game()
