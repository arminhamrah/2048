import random
import os
import sys
import tty
import termios

def clear_console():
    os.system('clear')

def print_board(board):
    clear_console()
    for row in board:
        print(" ".join(f"{tile:4}" if tile != 0 else "    " for tile in row))
    print("\nUse 'w' (up), 'a' (left), 's' (down), 'd' (right) to move. Press 'q' to quit.")

def spawn_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def move(board, direction):
    def merge(row):
        new_row = [tile for tile in row if tile != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [tile for tile in new_row if tile != 0]
        return new_row + [0] * (4 - len(new_row))

    if direction in 'LR':
        board = [merge(row) if direction == 'R' else merge(row[::-1])[::-1] for row in board]
    else:
        board = list(map(list, zip(*board)))
        board = [merge(row) if direction == 'D' else merge(row[::-1])[::-1] for row in board]
        board = list(map(list, zip(*board)))
    
    return board

def game_over(board):
    if any(0 in row for row in board):
        return False
    for i in range(4):
        for j in range(4):
            if (i < 3 and board[i][j] == board[i + 1][j]) or (j < 3 and board[i][j] == board[i][j + 1]):
                return False
    return True

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def check_2048(board):
    return any(2048 in row for row in board)

def play_2048():
    board = [[0 for _ in range(4)] for _ in range(4)]
    spawn_tile(board)
    spawn_tile(board)
    reached_2048 = False

    while True:
        print_board(board)
        move_input = getch().lower()

        if move_input == 'q':
            print("Thanks for playing!")
            break

        direction_map = {
            's': 'U',
            'd': 'L',
            'w': 'D',
            'a': 'R'
        }

        if move_input in direction_map:
            new_board = move(board, direction_map[move_input])
            if new_board != board:
                board = new_board
                spawn_tile(board)
                
                if check_2048(board) and not reached_2048:
                    print("Congratulations! You've reached 2048!")
                    reached_2048 = True
                    input("Press Enter to continue...")
                
                if game_over(board):
                    print_board(board)
                    print("Game Over!")
                    break
        elif move_input != 'q':
            print("Invalid move. Use 'w', 'a', 's', 'd' to move, 'q' to quit.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    play_2048()