# CECS 551 Assignment 3

## Minesweeper
This project involves building an AI agent that can play the classic game of Minesweeper. The agent uses propositional logic and a knowledge base to infer the locations of mines on the board and make safe moves.

## Background
>Minesweeper is a puzzle game where the player clicks on cells in a grid, trying to avoid the cells that contain hidden mines. Clicking on a cell that contains a mine causes the player to lose the game. Clicking on a safe cell reveals a number that indicates how many neighboring cells (cells that are one square to the left, right, up, down, or diagonal from the given cell) contain mines.

The goal of the game is to correctly identify all the mines on the board. The player can mark a cell as containing a mine by right-clicking on it.

## Implementation
The project involves implementing the following components:

1. **Sentence class**: This class represents a logical sentence about the Minesweeper board, containing a set of cells and a count of how many of those cells are mines.
   - Implements the `known_mines`, `known_safes`, `mark_mine`, and `mark_safe` methods.

2. **MinesweeperAI class**: This class represents the AI agent that plays the Minesweeper game.
   - Implements the `add_knowledge`, `make_safe_move`, and `make_random_move` methods.

The `add_knowledge` method updates the AI's knowledge base with new information about a safe cell and its neighboring mine count. The `make_safe_move` method returns a move that is known to be safe, and the `make_random_move` method returns a random, non-mine move.

## Getting Started
1. Install the required Python package (`pygame`) by running `pip3 install -r requirements.txt`.
3. Run the game using `python runner.py`.

## More Information
- The `known_mines` and `known_safes` functions in the `Sentence` class determines which cells in the sentence are known to be mines or safe, respectively.
- The `mark_mine` and `mark_safe` functions in the `Sentence` class updates the sentence when a cell is known to be a mine or safe.
- The `add_knowledge` function in the `MinesweeperAI` class updates the AI's knowledge base with new information about a safe cell and its neighboring mine count, and infer new information about safe and mine cells.
- The `make_safe_move` function in the `MinesweeperAI` class returns a move that is known to be safe, and the `make_random_move` function returns a random, non-mine move.