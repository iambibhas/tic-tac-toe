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
- 2 player game
  - can it support 2+ players? maybe for bigger matrix than 3x3
- There are 8 winning patterns for a 3x3 board
  - 10 winning patterns for 4x4. essentially, for a square of size `n`, there are `n*2+2` winning patterns
  - can these patterns be auto generated given the size of the square?
- Players take turn to play
  - if player X starts the game against player Y, any time it's the turn of player X, the number of cells occupied by Y must be one less than cells occupied by Y.
  - If it's the turn of Y, the number of cells occupied by X must be one more than the cells occupied by Y
  - one player cannot play two consecutive turns
- The game ends when one player has occupied a winning patterns, no further input allowed
- Once a cell is occupied, it is immutable
- When it's the turn of player X, player Y cannot send an input, the board has to be locked for Y
