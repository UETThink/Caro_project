# -*- coding: utf-8 -*-
"""
source/caro_game.py
Logic game cho cờ Caro: biểu diễn bàn cờ, luật chơi, sinh nước đi hợp lệ, kiểm tra trạng thái kết thúc
"""

import copy

# Kích thước bàn cờ (tối thiểu 9x9 theo yêu cầu)
BOARD_SIZE = 9

# Trạng thái ô cờ
EMPTY = 0
PLAYER_X = 1  # Người chơi (MAX)
PLAYER_O = -1  # Máy tính (MIN)

class CaroGame:
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.current_player = PLAYER_X  # Người đi trước
        self.last_move = None  # (row, col) của nước đi cuối
        self.move_count = 0
        self.winner = None
        self.game_over = False

    def reset(self):
        """Khởi tạo lại game"""
        self.board = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = PLAYER_X
        self.last_move = None
        self.move_count = 0
        self.winner = None
        self.game_over = False

    def copy(self):
        """Tạo bản sao của game state"""
        new_game = CaroGame(self.size)
        new_game.board = copy.deepcopy(self.board)
        new_game.current_player = self.current_player
        new_game.last_move = self.last_move
        new_game.move_count = self.move_count
        new_game.winner = self.winner
        new_game.game_over = self.game_over
        return new_game

    def set_state(self, board_state, current_player=PLAYER_X):
        """Đặt trạng thái bàn cờ từ ma trận cho trước"""
        self.board = copy.deepcopy(board_state)
        self.current_player = current_player
        self.move_count = sum(1 for row in board_state for cell in row if cell != EMPTY)
        # Tìm last_move
        for i in range(self.size):
            for j in range(self.size):
                if board_state[i][j] != EMPTY:
                    self.last_move = (i, j)

    def is_valid_move(self, row, col, check_empty=True):
        """
        Kiểm tra nước đi hợp lệ
        - row, col: tọa độ trên bàn cờ (0-indexed)
        - check_empty: True nếu cần kiểm tra ô trống
        """
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        if check_empty and self.board[row][col] != EMPTY:
            return False
        return True

    def make_move(self, row, col, player=None):
        """
        Thực hiện nước đi
        Returns: True nếu thành công, False nếu thất bại
        """
        if player is None:
            player = self.current_player

        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = player
        self.last_move = (row, col)
        self.move_count += 1

        # Kiểm tra thắng
        if self.check_win(row, col, player):
            self.winner = player
            self.game_over = True
        # Kiểm tra hòa
        elif self.move_count >= self.size * self.size:
            self.winner = 0
            self.game_over = True

        # Đổi lượt
        self.current_player = -self.current_player
        return True

    def undo_move(self, row, col):
        """Hoàn tác nước đi"""
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
        """Đếm số quân cùng màu liên tiếp theo một hướng"""
        count = 0
        r, c = row + d_row, col + d_col
        while (0 <= r < self.size and 0 <= c < self.size and
               self.board[r][c] == player):
            count += 1
            r += d_row
            c += d_col
        return count

    def check_win(self, row, col, player):
        """
        Kiểm tra thắng: 4 quân liên tiếp (không cần chặn 2 đầu theo yêu cầu)
        4 hướng: ngang, dọc, 2 đường chéo
        """
        # 4 hướng: (dr, dc)
        directions = [
            (0, 1),   # Ngang
            (1, 0),   # Dọc
            (1, 1),   # Chéo xuống
            (1, -1)   # Chéo lên
        ]

        for d_row, d_col in directions:
            # Đếm quân liên tiếp về 2 phía
            count = 1
            count += self.count_direction(row, col, d_row, d_col, player)
            count += self.count_direction(row, col, -d_row, -d_col, player)

            if count >= 4:
                return True
        return False

    def get_valid_moves(self):
        """
        Sinh danh sách nước đi hợp lệ
        Theo yêu cầu: chỉ xét các ô trống có quân cờ xung quanh (bound moves)
        """
        if self.move_count == 0:
            # Nước đi đầu tiên: giữa bàn cờ
            return [(self.size // 2, self.size // 2)]

        moves = set()

        # Tìm tất cả các ô có quân cờ và lấy các ô trống xung quanh
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != EMPTY:
                    # Kiểm tra 8 ô xung quanh
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if self.is_valid_move(ni, nj):
                                moves.add((ni, nj))

        # Sắp xếp theo thứ tự: ưu tiên gần last_move
        if self.last_move:
            last_r, last_c = self.last_move
            moves = sorted(moves, key=lambda m:
                abs(m[0] - last_r) + abs(m[1] - last_c))
        else:
            moves = sorted(moves)

        return list(moves)

    def get_all_valid_moves(self):
        """
        Lấy tất cả nước đi hợp lệ (không giới hạn bound)
        """
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == EMPTY:
                    moves.append((i, j))
        return moves

    def is_terminal(self):
        """Kiểm tra trạng thái kết thúc (thắng/thua/hòa)"""
        return self.game_over

    def get_result(self):
        """
        Lấy kết quả game:
        - 1: PLAYER_X thắng
        - -1: PLAYER_O thắng
        - 0: Hòa
        - None: Game chưa kết thúc
        """
        if self.winner is not None:
            return self.winner
        if self.move_count >= self.size * self.size:
            return 0
        return None

    def print_board(self):
        """In bàn cờ ra console"""
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
        """Chuyển bàn cờ thành string để debug"""
        symbols = {EMPTY: '.', PLAYER_X: 'X', PLAYER_O: 'O'}
        lines = []
        for row in self.board:
            line = " ".join(symbols[cell] for cell in row)
            lines.append(line)
        return "\n".join(lines)


def create_test_state_1():
    """Trạng thái đầu ván"""
    game = CaroGame()
    return game


def create_test_state_2():
    """Trạng thái giữa ván - người đi trước đã đánh vài nước"""
    game = CaroGame()
    moves = [(4, 4), (3, 3), (4, 3), (5, 5), (3, 4)]
    for i, (r, c) in enumerate(moves):
        player = PLAYER_X if i % 2 == 0 else PLAYER_O
        game.make_move(r, c, player)
    return game


def create_test_state_3():
    """Trạng thái máy sắp thắng - cần tấn công"""
    game = CaroGame()
    # Máy (O) có 3 quân liên tiếp, cần đánh nước thắng
    game.board[4][4] = PLAYER_O
    game.board[4][5] = PLAYER_O
    game.board[4][6] = PLAYER_O
    game.current_player = PLAYER_O
    game.move_count = 3
    return game


def create_test_state_4():
    """Trạng thái người sắp thắng - máy cần chặn"""
    game = CaroGame()
    # Người (X) có 3 quân liên tiếp, máy cần chặn
    game.board[3][3] = PLAYER_X
    game.board[3][4] = PLAYER_X
    game.board[3][5] = PLAYER_X
    game.current_player = PLAYER_O  # Lượt máy
    game.move_count = 3
    return game


def create_test_state_5():
    """Trạng thái hai bên đều có cơ hội tấn công"""
    game = CaroGame()
    # Người có 2 quân ngang
    game.board[2][2] = PLAYER_X
    game.board[2][3] = PLAYER_X
    # Máy có 2 quân dọc
    game.board[5][5] = PLAYER_O
    game.board[6][5] = PLAYER_O
    game.current_player = PLAYER_O
    game.move_count = 4
    return game


def create_test_state_6():
    """Trạng thái phức tạp - nhiều nước đi tiềm năng"""
    game = CaroGame()
    # Tạo nhiều chuỗi 2-3 quân để test
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
