def check_winning_move_possible(board):
    ROWS = 6
    COLUMNS = 7

    for r in range(ROWS - 1):
        for c in range(COLUMNS - 1):
            # Check each 2x2 square grid
            square = [board[r][c], board[r][c + 1], board[r + 1][c], board[r + 1][c + 1]]

            # Count the number of 'X' and 'O' pieces in the square
            x_count = square.count('X')
            o_count = square.count('O')
            empty_count = square.count(' ')

            # Check if there are 3 pieces of the same kind and 1 empty slot in the square
            if (x_count == 3 and empty_count == 1) or (o_count == 3 and empty_count == 1):
                print("Winning move possible")

            # If no winning move found in any 2x2 square
            else:
                print("Winning move not possible")


# Example usage:
# Create a 6x7 Connect 4 board and populate it with 'X', 'O', and empty slots
board = [
    ['X', ' ', 'X', 'O', 'X', 'O', 'X'],
    ['O', 'X', 'O', 'X', 'O', 'X', 'O'],
    ['X', 'O', 'X', 'O', 'X', 'O', 'X'],
    ['O', 'X', 'O', 'X', 'O', 'X', 'O'],
    ['X', 'O', 'X', 'O', 'X', 'O', 'X'],
    ['O', 'X', 'O', 'X', 'O', 'X', 'O']
]

check_winning_move_possible(board)
