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
