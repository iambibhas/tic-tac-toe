# Tic-Tac-Toe

Two player tic-tac-toe.

Requires Python 3.6+.

### To play

Run this command to start a 2 player game, where each player take turn to input their position -
```
python3 tictactoe.py
```

To play against the AI, run
```
python3 tictactoe.py --against-ai
```
or
```
python3 tictactoe.py -a
```

### To test
```
pip install -r test_requirements.txt
pytest
```

### Assumptions
- 2 player game, 3x3 board
- In the AI mode, Player 2 is assumed to be the AI
- There are 8 winning patterns for a 3x3 board
  - 10 winning patterns for 4x4. essentially, for a square of size `n`, there are `n*2+2` winning patterns
  - these patterns can be auto generated given the size of the square
- Players take turn to play, one player cannot play two consecutive turns
- The game ends when one player has occupied a winning patterns, no further input allowed
- Once a cell is occupied, it is immutable, picking that posistion will ask for valid input
- When it's the turn of player X, player Y cannot send an input, the board has to be locked for Y


### Limitations
- Some of the code is written to optimize for a 3x3 game, e.g.
  - the minimax function doesn't consider the depth of search, it searches everything
  - to accommdate a larger board, a depth parameter can be added to the search algorithm, so that it makes a reasonably well thought play, if not optimal
  - have not tried it, but I think the depth param can be also configured to create a difficulty setting, in lower difficulty, the minimax algorithm will search lower amount of depth and vice versa
- the minimax function assumes one player is a real person. Can't accommodate 2 Ai players playing against each other right now.
  - in the current version of the code, player X is always the minimizer and player O is always the maximizer
  - to accommodate 2 AI players playing each other, the minimax function will need to accept a `current_player` argument and create a new state where the current player will be the maximizer and the other player will be the minimizer
