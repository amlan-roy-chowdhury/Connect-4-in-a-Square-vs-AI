import math
import random
import time
from tkinter import Canvas, IntVar, Scale, StringVar, Tk
from tkinter.ttk import Button, Combobox, Entry, Label, Radiobutton

import numpy as np

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 2

COLOR_CHOICES = {
    "Tan": "#E6DBAC",
    "Beige": "#EEDC9A",
    "Macaroon": "#F9E076",
    "Hazel Wood": "#C9BB8E",
    "Granola": "#D6B85A",
    "Oat": "#DFC98A",
    "Egg Nog": "#FAE29C",
    "Fawn": "#C8A951",
    "Sugar Cookie": "#F3EAAF",
    "Sand": "#D8B863",
    "Sepia": "#E3B778",
    "Latte": "#E7C27D",
    "Oyster": "#DCD7A0",
    "Biscotti": "#E3C565",
    "Parmesan": "#FDE992",
    "Hazelnut": "#BDA55D",
}

CANVAS_DIMS = (400, 300)
CANVAS_BG = "#E6DBAC"
GRID_WIDTH = 7
GRID_HEIGHT = 6
SQUARESIZE = 50
DISC_COLORS = {AI_PIECE: "white", PLAYER_PIECE: "black"}


class Game:
    def __init__(self):
        self.root = Tk()
        self.root.title("Connect 4 Game")
        self.root.configure(bg="light gray")
        self.canvas = Canvas(
            self.root,
            width=CANVAS_DIMS[0],
            height=CANVAS_DIMS[1],
            bg=CANVAS_BG,
        )
        self.init_data()
        self.init_widgets()
        self.draw_board()
        self.register_handlers()
        self.root.mainloop()

    def init_data(self):
        # Inits data for the game
        self.board_color = StringVar(value=list(COLOR_CHOICES.keys())[0])
        self.player_name = StringVar(value="NAME")
        self.first_player = IntVar(value=PLAYER)
        self.agent_level = IntVar(value=3)
        self.disable_inputs = True

    def game_init(self):
        # Inits/Starts the game
        self.start = time.time()
        self.disable_inputs = False
        self.board = self.create_board()
        self.level = self.agent_level.get()
        self.turn = self.first_player.get()
        self.player_discs = 0
        self.ai_discs = 0
        if self.turn != PLAYER:
            self.play_agent()

    def init_widgets(self):
        # Inits all the widgets
        self.color_label = Label(self.root, text="Select Board Color:")
        self.color_option = Combobox(
            self.root,
            values=list(COLOR_CHOICES.keys()),
            textvariable=self.board_color,
        )
        self.player_name_label = Label(self.root, text="Enter Player's Name:")
        self.player_name_entry = Entry(
            self.root,
            textvariable=self.player_name,
        )

        self.first_player_label = Label(self.root, text="Select First Player:")
        self.first_player_options = [
            Radiobutton(
                self.root,
                text="Human",
                variable=self.first_player,
                value=0,
            ),
            Radiobutton(
                self.root,
                text="Agent",
                variable=self.first_player,
                value=1,
            ),
        ]

        self.agent_level_label = Label(
            self.root, text="Agent's Intelligence Level [1-5]:"
        )
        self.agent_level_scale = Scale(
            self.root,
            variable=self.agent_level,
            from_=1,
            to=5,
            orient="horizontal",
        )

        self.start_button = Button(
            self.root, text="Start Game", command=lambda: self.game_init()
        )
        self.result_label = Label(self.root, text="")
        self.moves_label = Label(self.root, text="")

        # Layout widgets using a grid
        self.color_label.grid(row=0, column=0, sticky="w")
        self.color_option.grid(row=0, column=1, sticky="w")
        self.player_name_label.grid(row=1, column=0, sticky="w")
        self.player_name_entry.grid(row=1, column=1, sticky="w")
        self.first_player_label.grid(row=2, column=0, sticky="w")
        self.first_player_options[0].grid(row=2, column=1, sticky="w")
        self.first_player_options[1].grid(row=3, column=1, sticky="w")
        self.agent_level_label.grid(row=4, column=0, sticky="w")
        self.agent_level_scale.grid(row=4, column=1, sticky="w")
        self.start_button.grid(row=5, columnspan=2)
        self.result_label.grid(row=6, columnspan=2)
        self.moves_label.grid(row=7, columnspan=2)
        self.canvas.grid(row=0, column=2, rowspan=8)

    def register_handlers(self):
        # Color change
        self.color_option.bind(
            "<<ComboboxSelected>>",
            lambda _: self.canvas.configure(
                bg=COLOR_CHOICES[self.color_option.get()]
            ),
        )
        # Player drops
        self.canvas.bind("<Button-1>", lambda e: self.drop_piece_gui(e))
        # Start
        self.start_button.bind("<Button-1>", lambda e: self.game_init())

    def draw_board(self):
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                x1, y1 = col * SQUARESIZE, row * SQUARESIZE
                x2, y2 = x1 + SQUARESIZE, y1 + SQUARESIZE
                self.canvas.create_oval(
                    x1, y1, x2, y2, outline="black", fill="light gray"
                )

    def drop_piece_gui(self, e):
        if self.disable_inputs:
            return
        col = e.x // SQUARESIZE
        if Game.is_valid_location(self.board, col):
            row = Game.get_next_open_row(self.board, col)
            Game.drop_piece(self.board, row, col, PLAYER_PIECE)
            self.player_discs += 1
            self.update_disc_counts()
            # Game.print_board(self.board)
            self.color_oval(row, col, PLAYER_PIECE)
            self.next_turn()
            self.play_agent()

    def play_agent(self):
        # AI Turn
        col, minmax_score = Game.minimax(
            self.board,
            self.agent_level.get(),
            -math.inf,
            math.inf,
            True,
        )
        if col is None:
            self.next_turn()
        if Game.is_valid_location(self.board, col):
            row = Game.get_next_open_row(self.board, col)
            Game.drop_piece(self.board, row, col, AI_PIECE)
            self.ai_discs += 1
            self.update_disc_counts()
            self.color_oval(row, col, AI_PIECE)
            self.next_turn()

    def update_disc_counts(self):
        self.moves_label.config(
            text=f"Number of Moves: {self.player_discs + self.ai_discs}"
        )

    def next_turn(self):
        if Game.winning_move(self.board, AI_PIECE):
            self.result_label.config(
                text=f"Winner: Agent\nGame Duration: {round(time.time() - self.start, 2)} seconds",
            )
            self.disable_inputs = True
            return
        if Game.winning_move(self.board, PLAYER_PIECE):
            self.result_label.config(
                text=f"Winner: {self.player_name.get()}\nGame Duration: {round(time.time() - self.start, 2)} seconds",
            )
            self.disable_inputs = True
            return
        if Game.is_terminal_node(self.board):
            self.result_label.config(
                text=f"DRAW\nGame Duration: {round(time.time() - self.start, 2)} seconds",
            )
            self.disable_inputs = True
            return
        self.turn = (self.turn + 1) % 2

    def color_oval(self, row, col, piece):
        x1, y1 = col * SQUARESIZE, row * SQUARESIZE
        x2, y2 = x1 + SQUARESIZE, y1 + SQUARESIZE
        self.canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            outline="black",
            fill=DISC_COLORS[piece],
        )

    # connect4_with_ai with modifications below

    @staticmethod
    def create_board():
        return np.zeros((ROW_COUNT, COLUMN_COUNT))

    @staticmethod
    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    @staticmethod
    def is_valid_location(board, col):
        return board[0][col] == 0

    @staticmethod
    def get_next_open_row(board, col):
        for r in range(ROW_COUNT - 1, -1, -1):
            if board[r][col] == 0:
                return r

    @staticmethod
    def print_board(board):
        # print(np.flip(board, 0))
        print(board)

    @staticmethod
    def winning_move(board, piece):
        for r in range(ROW_COUNT - 1):
            for c in range(COLUMN_COUNT - 1):
                # Check each 2x2 square grid
                square = [
                    board[r][c],
                    board[r][c + 1],
                    board[r + 1][c],
                    board[r + 1][c + 1],
                ]
                if square.count(piece) == 4:
                    return True
        return False

    @staticmethod
    def evaluate_window(window, piece):
        score = 0
        opp_piece = PLAYER_PIECE
        if piece == PLAYER_PIECE:
            opp_piece = AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    @staticmethod
    def score_position(board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3
        #
        # # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 1):
                window = row_array[c : c + WINDOW_LENGTH]
                score += Game.evaluate_window(window, piece)
        #
        # # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 1):
                window = col_array[r : r + WINDOW_LENGTH]
                score += Game.evaluate_window(window, piece)

        return score

    @staticmethod
    def is_terminal_node(board):
        return (
            Game.winning_move(board, PLAYER_PIECE)
            or Game.winning_move(board, AI_PIECE)
            or len(Game.get_valid_locations(board)) == 0
        )

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizingPlayer):
        valid_locations = Game.get_valid_locations(board)
        is_terminal = Game.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if Game.winning_move(board, AI_PIECE):
                    return (None, 100000000000000)
                elif Game.winning_move(board, PLAYER_PIECE):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, Game.score_position(board, AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = Game.get_next_open_row(board, col)
                b_copy = board.copy()
                Game.drop_piece(b_copy, row, col, AI_PIECE)
                new_score = Game.minimax(
                    b_copy,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                )[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = Game.get_next_open_row(board, col)
                b_copy = board.copy()
                Game.drop_piece(b_copy, row, col, PLAYER_PIECE)
                new_score = Game.minimax(b_copy, depth - 1, alpha, beta, True)[
                    1
                ]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    @staticmethod
    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if Game.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    @staticmethod
    def pick_best_move(board, piece):
        valid_locations = Game.get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = Game.get_next_open_row(board, col)
            temp_board = board.copy()
            Game.drop_piece(temp_board, row, col, piece)
            score = Game.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col


if __name__ == "__main__":
    Game()
