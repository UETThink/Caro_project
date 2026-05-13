# -*- coding: utf-8 -*-
import copy

BOARD_SIZE = 9

EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1

class CaroGame:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.current_player = PLAYER_X
        self.last_move = None
        self.move_count = 0
        self.winner = None
        self.game_over = False

    def reset(self):
        self.board = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = PLAYER_X
        self.last_move = None
        self.move_count = 0
        self.winner = None
        self.game_over = False

    def copy(self):
        new_game = CaroGame(self.size)
        new_game.board = copy.deepcopy(self.board)
        new_game.current_player = self.current_player
        new_game.last_move = self.last_move
        new_game.move_count = self.move_count
        new_game.winner = self.winner
        new_game.game_over = self.game_over
        return new_game

    def set_state(self, board_state, current_player=PLAYER_X):
        self.board = copy.deepcopy(board_state)
        self.current_player = current_player
        self.move_count = sum(1 for row in board_state for cell in row if cell != EMPTY)
        for i in range(self.size):
            for j in range(self.size):
                if board_state[i][j] != EMPTY:
                    self.last_move = (i, j)

    def is_valid_move(self, row, col, check_empty=True):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        if check_empty and self.board[row][col] != EMPTY:
            return False
        return True

    def make_move(self, row, col, player=None):
        if player is None:
            player = self.current_player

        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = player
        self.last_move = (row, col)
        self.move_count += 1

        if self.check_win(row, col, player):
            self.winner = player
            self.game_over = True
        elif self.move_count >= self.size * self.size:
            self.winner = 0
            self.game_over = True

        self.current_player = -self.current_player
        return True

    def undo_move(self, row, col):
        if self.board[row][col] == EMPTY:
            return False
        self.board[row][col] = EMPTY
        self.move_count -= 1
        self.current_player = -self.current_player
        self.last_move = None
        self.winner = None
        self.game_over = False
        return True

    def count_direction(self, row, col, d_row, d_col, player):
        count = 0
        r, c = row + d_row, col + d_col
        while (0 <= r < self.size and 0 <= c < self.size and
               self.board[r][c] == player):
            count += 1
            r += d_row
            c += d_col
        return count

    def check_win(self, row, col, player):
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for d_row, d_col in directions:
            count = 1
            count += self.count_direction(row, col, d_row, d_col, player)
            count += self.count_direction(row, col, -d_row, -d_col, player)

            if count >= 4:
                return True
        return False

    def get_valid_moves(self):
        if self.move_count == 0:
            return [(self.size // 2, self.size // 2)]

        moves = set()

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != EMPTY:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if self.is_valid_move(ni, nj):
                                moves.add((ni, nj))

        if self.last_move:
            last_r, last_c = self.last_move
            moves = sorted(moves, key=lambda m:
                abs(m[0] - last_r) + abs(m[1] - last_c))
        else:
            moves = sorted(moves)

        return list(moves)

    def get_all_valid_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == EMPTY:
                    moves.append((i, j))
        return moves

    def is_terminal(self):
        return self.game_over

    def get_result(self):
        if self.winner is not None:
            return self.winner
        if self.move_count >= self.size * self.size:
            return 0
        return None

    def print_board(self):
        symbols = {EMPTY: '.', PLAYER_X: 'X', PLAYER_O: 'O'}
        print("  ", end="")
        for j in range(self.size):
            print(j, end=" ")
        print()
        for i, row in enumerate(self.board):
            print(i, end=" ")
            for cell in row:
                print(symbols[cell], end=" ")
            print()
        print()

    def board_to_string(self):
        symbols = {EMPTY: '.', PLAYER_X: 'X', PLAYER_O: 'O'}
        lines = []
        for row in self.board:
            line = " ".join(symbols[cell] for cell in row)
            lines.append(line)
        return "\n".join(lines)


def create_test_state_1():
    game = CaroGame()
    return game


def create_test_state_2():
    game = CaroGame()
    moves = [(4, 4), (3, 3), (4, 3), (5, 5), (3, 4)]
    for i, (r, c) in enumerate(moves):
        player = PLAYER_X if i % 2 == 0 else PLAYER_O
        game.make_move(r, c, player)
    return game


def create_test_state_3():
    game = CaroGame()
    game.board[4][4] = PLAYER_O
    game.board[4][5] = PLAYER_O
    game.board[4][6] = PLAYER_O
    game.current_player = PLAYER_O
    game.move_count = 3
    return game


def create_test_state_4():
    game = CaroGame()
    game.board[3][3] = PLAYER_X
    game.board[3][4] = PLAYER_X
    game.board[3][5] = PLAYER_X
    game.current_player = PLAYER_O
    game.move_count = 3
    return game


def create_test_state_5():
    game = CaroGame()
    game.board[2][2] = PLAYER_X
    game.board[2][3] = PLAYER_X
    game.board[5][5] = PLAYER_O
    game.board[6][5] = PLAYER_O
    game.current_player = PLAYER_O
    game.move_count = 4
    return game


def create_test_state_6():
    game = CaroGame()
    game.board[0][0] = PLAYER_X
    game.board[1][1] = PLAYER_X
    game.board[2][2] = PLAYER_X

    game.board[7][7] = PLAYER_O
    game.board[6][6] = PLAYER_O

    game.board[4][0] = PLAYER_X
    game.board[5][0] = PLAYER_X

    game.board[0][7] = PLAYER_O
    game.board[1][7] = PLAYER_O
    game.board[2][7] = PLAYER_O

    game.current_player = PLAYER_O
    game.move_count = 9
    return game
