import random
from .board import board, SIZE

def add_tile():
    """Add a new tile (either 2 or 4) to the board"""
    # Choose a random empty cell
    empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if len(empty_cells) == 0:
        return False
    row, col = random.choice(empty_cells)
    # Choose a random value (either 2 or 4)
    value = random.choice([2, 4])
    board[row][col] = value
    return True

def merge(row):
    """Merge tiles in a single row"""
    # Remove any zeros from the row
    row = [tile for tile in row if tile != 0]
    # Merge any adjacent tiles with the same value
    i = 0
    while i < len(row) - 1:
        if row[i] == row[i + 1]:
            row[i] = row[i] * 2
            row.pop(i + 1)
        i += 1
    # Pad with zeros to maintain the original length
    while len(row) < SIZE:
        row.append(0)
    return row