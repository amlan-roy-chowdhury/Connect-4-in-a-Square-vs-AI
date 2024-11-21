import numpy as np

# Define the game board dimensions, player and AI
rows = 6
cols = 7
Player = 1
AI = 2

LEVELS = [1, 2, 3, 4, 5]


# Function to initialize the game board
def create_board():
    return np.zeros((rows, cols))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[rows - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r


def is_winning_move (board, row, col, piece):
def ai_move(board, level):
    if level == 1:
        return minimax(board, 1, -np.inf, np.inf, True)[0]
    elif level == 2:
        return minimax(board, 2, -np.inf, np.inf, True)[0]
    elif level == 3:
        return minimax(board, 3, -np.inf, np.inf, True)[0]
    elif level == 4:
        return minimax(board, 4, -np.inf, np.inf, True)[0]
    elif level == 5:
        return minimax(board, 5, -np.inf, np.inf, True)[0]


def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = [c for c in range(cols) if is_valid_location(board, c)]

    if depth == 0 or is_terminal_node(board):
        if depth == 0:
            return (None, evaluate_board(board, AI))
        elif is_winning_move(board, ROWS - 1, valid_locations[0], Player):
            return (None, -np.inf)
        elif is_winning_move(board, ROWS - 1, valid_locations[0], AI):
            return (None, np.inf)
        else:
            return (None, 0)

    if maximizing_player:
        value = -np.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = np.inf
        best_col = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, Player)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


def is_terminal_node(board):
    return is_winning_move(board, rows - 1, get_next_open_row(board, 0), Player) or \
        is_winning_move(board, rows - 1, get_next_open_row(board, 0), AI) or \
        len([c for c in range(COLS) if is_valid_location(board, c)]) == 0


def evaluate_board(board, piece):
    score = 0
    opp_piece = Player if piece == AI else AI

    # Score center column
    center_array = [int(i) for i in list(board[:, cols // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(rows):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(cols - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece, opp_piece)

    # Score vertical
    for c in range(cols):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rows - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece, opp_piece)

    # Score positive diagonal
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece, opp_piece)

    # Score negative diagonal
    for r in range(3, rows):
        for c in range(cols - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece, opp_piece)

    return score


def evaluate_window(window, piece, opp_piece):
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4
    return score


# Sample usage
board = create_board()
level = 3
while not is_terminal_node(board):
    if level % 2 == 1:  # Human's turn
        col = int(input("Enter your move (1-7): ")) - 1
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, Player)
    else:  # AI's turn
        col = ai_move(board, level)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI)
    print_board(board)