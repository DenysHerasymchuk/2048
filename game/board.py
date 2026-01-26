import random

# Define the size of the board
SIZE = 4

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