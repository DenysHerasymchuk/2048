import random
from .constants import GRID_SIZE, WINNING_TILE


class Board:
    """Manages the 2048 game board state."""

    def __init__(self):
        self.size = GRID_SIZE
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.best_score = 0
        self.game_over = False
        self.won = False
        self.keep_playing = False

    def reset(self):
        """Reset the board for a new game."""
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.keep_playing = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell."""
        empty_cells = [
            (i, j)
            for i in range(self.size)
            for j in range(self.size)
            if self.grid[i][j] == 0
        ]

        if not empty_cells:
            return False

        row, col = random.choice(empty_cells)
        # 90% chance of 2, 10% chance of 4
        self.grid[row][col] = 2 if random.random() < 0.9 else 4
        return True

    def get_cell(self, row, col):
        """Get the value at a specific cell."""
        return self.grid[row][col]

    def set_cell(self, row, col, value):
        """Set the value at a specific cell."""
        self.grid[row][col] = value

    def clone(self):
        """Create a copy of the current board state."""
        new_board = Board()
        new_board.grid = [row[:] for row in self.grid]
        new_board.score = self.score
        new_board.best_score = self.best_score
        new_board.game_over = self.game_over
        new_board.won = self.won
        new_board.keep_playing = self.keep_playing
        return new_board

    def has_won(self):
        """Check if the player has reached 2048."""
        if self.keep_playing:
            return False
        for row in self.grid:
            if WINNING_TILE in row:
                return True
        return False

    def can_move(self):
        """Check if any moves are possible."""
        # Check for empty cells
        for row in self.grid:
            if 0 in row:
                return True

        # Check for possible merges horizontally
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return True

        # Check for possible merges vertically
        for i in range(self.size - 1):
            for j in range(self.size):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return True

        return False

    def update_best_score(self):
        """Update the best score if current score is higher."""
        if self.score > self.best_score:
            self.best_score = self.score
