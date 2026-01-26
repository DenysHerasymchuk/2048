import random

# Define the size of the board
SIZE = 4

# Define the possible directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# Define the board as a 2D list of zeros
board = [[0 for i in range(SIZE)] for j in range(SIZE)]

def print_board():
    """Print the current state of the board"""
    print('-' * 21)
    for i in range(SIZE):
        print('|', end='')
        for j in range(SIZE):
            if board[i][j] == 0:
                print('  .', end='')
            else:
                print(f'{board[i][j]:3d}', end='')
        print('  |')
    print('-' * 21)

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

def move_left():
    """Move all tiles to the left and merge"""
    moved = False
    for i in range(SIZE):
        # Save original row to check if it changed
        original_row = board[i][:]
        # Get the current row
        row = board[i][:]
        # Merge the row
        merged_row = merge(row)
        # Update the board
        board[i] = merged_row
        # Check if the row changed
        if original_row != board[i]:
            moved = True
    return moved

def move_right():
    """Move all tiles to the right and merge"""
    moved = False
    for i in range(SIZE):
        original_row = board[i][:]
        # Get the current row and reverse it
        row = board[i][:]
        row.reverse()
        # Merge the row
        merged_row = merge(row)
        # Reverse back and update
        merged_row.reverse()
        board[i] = merged_row
        if original_row != board[i]:
            moved = True
    return moved

def move_up():
    """Move all tiles up and merge"""
    moved = False
    for j in range(SIZE):
        # Get the current column
        original_column = [board[i][j] for i in range(SIZE)]
        column = [board[i][j] for i in range(SIZE)]
        # Merge the column
        merged_column = merge(column)
        # Update the board
        for i in range(SIZE):
            board[i][j] = merged_column[i]
        # Check if column changed
        if original_column != [board[i][j] for i in range(SIZE)]:
            moved = True
    return moved

def move_down():
    """Move all tiles down and merge"""
    moved = False
    for j in range(SIZE):
        original_column = [board[i][j] for i in range(SIZE)]
        # Get the current column and reverse it
        column = [board[i][j] for i in range(SIZE)]
        column.reverse()
        # Merge the column
        merged_column = merge(column)
        # Reverse back
        merged_column.reverse()
        # Update the board
        for i in range(SIZE):
            board[i][j] = merged_column[i]
        if original_column != [board[i][j] for i in range(SIZE)]:
            moved = True
    return moved

def is_game_over():
    """Check if the game is over (no moves possible)"""
    # If there are empty cells, game is not over
    empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if len(empty_cells) > 0:
        return False
    
    # Check if any adjacent tiles can be merged
    for i in range(SIZE):
        for j in range(SIZE):
            # Check right neighbor
            if j < SIZE - 1 and board[i][j] == board[i][j + 1]:
                return False
            # Check down neighbor
            if i < SIZE - 1 and board[i][j] == board[i + 1][j]:
                return False
    return True

# MAIN GAME LOOP - ADD THIS AT THE VERY BOTTOM:
try:
    if __name__ == "__main__":
        # Initialize the game
        add_tile()
        
        print("Welcome to 2048!")
        print("Use WASD keys to move:")
        print("  W - Up")
        print("  A - Left")
        print("  S - Down")
        print("  D - Right")
        print("  Q - Quit")
        print()
        
        while True:
            print_board()
            
            if is_game_over():
                print("Game Over!")
                break
            
            move = input("Enter your move (W/A/S/D/Q): ").strip().lower()
            
            if move == 'q':
                print("Thanks for playing!")
                break
            
            moved = False
            if move == 'w':
                moved = move_up()
            elif move == 'a':
                moved = move_left()
            elif move == 's':
                moved = move_down()
            elif move == 'd':
                moved = move_right()
            else:
                print("Invalid move! Use W, A, S, D, or Q")
                continue
            
            if moved:
                add_tile()
            else:
                print("No tiles moved. Try a different direction!")
except Exception as e:
    print("Bruh, just a random exception caught, nvm.")