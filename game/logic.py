import random
from .constants import GRID_SIZE, UP, DOWN, LEFT, RIGHT


class Move:
    """Represents a tile movement for animation."""
    def __init__(self, from_row, from_col, to_row, to_col, value, merged=False):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.value = value
        self.merged = merged


class GameLogic:
    """Handles the game logic for 2048."""

    def __init__(self, board):
        self.board = board
        self.last_moves = []
        self.new_tile_pos = None
        self.old_grid = None

    def move(self, direction):
        """Execute a move in the given direction. Returns True if the board changed."""
        # Save old state for animation
        self.old_grid = [row[:] for row in self.board.grid]
        self.last_moves = []

        moved = False

        if direction == UP:
            moved = self._move_up()
        elif direction == DOWN:
            moved = self._move_down()
        elif direction == LEFT:
            moved = self._move_left()
        elif direction == RIGHT:
            moved = self._move_right()

        if moved:
            self._add_random_tile()
            self.board.update_best_score()

            # Check win condition
            if self.board.has_won():
                self.board.won = True

            # Check game over
            if not self.board.can_move():
                self.board.game_over = True

        return moved

    def _move_left(self):
        """Move all tiles left."""
        moved = False
        for i in range(GRID_SIZE):
            row = self.board.grid[i]
            new_row, row_moves, row_moved = self._merge_line(row, i, 'row')
            if row_moved:
                moved = True
                self.board.grid[i] = new_row
                self.last_moves.extend(row_moves)
        return moved

    def _move_right(self):
        """Move all tiles right."""
        moved = False
        for i in range(GRID_SIZE):
            row = self.board.grid[i][::-1]
            new_row, row_moves, row_moved = self._merge_line(row, i, 'row', reverse=True)
            if row_moved:
                moved = True
                self.board.grid[i] = new_row[::-1]
                self.last_moves.extend(row_moves)
        return moved

    def _move_up(self):
        """Move all tiles up."""
        moved = False
        for j in range(GRID_SIZE):
            col = [self.board.grid[i][j] for i in range(GRID_SIZE)]
            new_col, col_moves, col_moved = self._merge_line(col, j, 'col')
            if col_moved:
                moved = True
                for i in range(GRID_SIZE):
                    self.board.grid[i][j] = new_col[i]
                self.last_moves.extend(col_moves)
        return moved

    def _move_down(self):
        """Move all tiles down."""
        moved = False
        for j in range(GRID_SIZE):
            col = [self.board.grid[i][j] for i in range(GRID_SIZE)][::-1]
            new_col, col_moves, col_moved = self._merge_line(col, j, 'col', reverse=True)
            if col_moved:
                moved = True
                new_col = new_col[::-1]
                for i in range(GRID_SIZE):
                    self.board.grid[i][j] = new_col[i]
                self.last_moves.extend(col_moves)
        return moved

    def _merge_line(self, line, index, line_type, reverse=False):
        """
        Merge a single line (row or column).
        Returns (new_line, moves, moved).
        """
        moves = []
        original = line[:]
        size = len(line)

        # Remove zeros and compact
        non_zero = [(i, val) for i, val in enumerate(line) if val != 0]

        # Track where each tile moves to
        new_line = [0] * size
        new_pos = 0
        i = 0

        while i < len(non_zero):
            orig_idx, val = non_zero[i]

            # Check if we can merge with the next tile
            if i + 1 < len(non_zero) and non_zero[i + 1][1] == val:
                # Merge tiles
                merged_val = val * 2
                self.board.score += merged_val
                new_line[new_pos] = merged_val

                # Record moves for both tiles
                next_orig_idx = non_zero[i + 1][0]

                if line_type == 'row':
                    if reverse:
                        from_pos1 = (index, size - 1 - orig_idx)
                        from_pos2 = (index, size - 1 - next_orig_idx)
                        to_pos = (index, size - 1 - new_pos)
                    else:
                        from_pos1 = (index, orig_idx)
                        from_pos2 = (index, next_orig_idx)
                        to_pos = (index, new_pos)
                else:  # column
                    if reverse:
                        from_pos1 = (size - 1 - orig_idx, index)
                        from_pos2 = (size - 1 - next_orig_idx, index)
                        to_pos = (size - 1 - new_pos, index)
                    else:
                        from_pos1 = (orig_idx, index)
                        from_pos2 = (next_orig_idx, index)
                        to_pos = (new_pos, index)

                moves.append(Move(from_pos1[0], from_pos1[1], to_pos[0], to_pos[1], val, True))
                moves.append(Move(from_pos2[0], from_pos2[1], to_pos[0], to_pos[1], val, True))

                i += 2
            else:
                # Just move the tile
                new_line[new_pos] = val

                if line_type == 'row':
                    if reverse:
                        from_pos = (index, size - 1 - orig_idx)
                        to_pos = (index, size - 1 - new_pos)
                    else:
                        from_pos = (index, orig_idx)
                        to_pos = (index, new_pos)
                else:  # column
                    if reverse:
                        from_pos = (size - 1 - orig_idx, index)
                        to_pos = (size - 1 - new_pos, index)
                    else:
                        from_pos = (orig_idx, index)
                        to_pos = (new_pos, index)

                if from_pos != to_pos:
                    moves.append(Move(from_pos[0], from_pos[1], to_pos[0], to_pos[1], val, False))

                i += 1

            new_pos += 1

        moved = new_line != original
        return new_line, moves, moved

    def _add_random_tile(self):
        """Add a random tile and record its position."""
        empty_cells = [
            (i, j)
            for i in range(GRID_SIZE)
            for j in range(GRID_SIZE)
            if self.board.grid[i][j] == 0
        ]

        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board.grid[row][col] = 2 if random.random() < 0.9 else 4
            self.new_tile_pos = (row, col)
        else:
            self.new_tile_pos = None
