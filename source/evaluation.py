"""
source/evaluation.py
Hàm đánh giá trạng thái bàn cờ cho thuật toán Minimax/Alpha-Beta
"""

from source.caro_game import BOARD_SIZE, EMPTY, PLAYER_X, PLAYER_O

# ============================================
# CÁC PATTERN VÀ ĐIỂM SỐ
# ============================================

# Điểm số cho các pattern (cho mỗi bên)
PATTERN_SCORES = {
    # Pattern 4 quân: THẮNG
    "four": 10000,

    # Pattern 3 quân liên tiếp (Live 3) - có thể tạo 4
    "live_three": 1000,

    # Pattern 3 bị chặn một đầu (Dead 3) - ít giá trị hơn
    "dead_three": 100,

    # Pattern 2 quân liên tiếp (Live 2) - cơ hội tấn công
    "live_two": 100,

    # Pattern 2 có khoảng trống (Spread 2)
    "spread_two": 50,

    # Pattern bị chặn 2 đầu (Dead 2)
    "dead_two": 10,

    # Điểm cho vị trí trung tâm - ưu tiên chiếm giữa bàn
    "center_bonus": 5,

    # Điểm cho nước đi gần quân đã đánh
    "adjacent_bonus": 1,
}


def evaluate_position(game, row, col, player):
    """
    Đánh giá giá trị của một nước đi cụ thể tại (row, col)
    cho player.
    """
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for d_row, d_col in directions:
        line = get_line(game, row, col, d_row, d_col, player)
        pattern_score = evaluate_line(line, player)
        score += pattern_score

    return score


def get_line(game, row, col, d_row, d_col, player):
    """
    Lấy chuỗi 7 ô: 3 ô trước, ô hiện tại, 3 ô sau
    theo hướng (d_row, d_col)
    """
    line = []
    count_before = 0
    count_after = 0

    # Lấy 3 ô trước
    r, c = row - d_row, col - d_col
    while count_before < 3 and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        line.insert(0, game.board[r][c])
        count_before += 1
        r -= d_row
        c -= d_col

    # Thêm ô hiện tại
    line.append(player)  # Giả sử đánh tại đây

    # Lấy 3 ô sau
    r, c = row + d_row, col + d_col
    while count_after < 3 and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        line.append(game.board[r][c])
        count_after += 1
        r += d_row
        c += d_col

    # Pad nếu không đủ 7 ô
    while len(line) < 7:
        if len(line) < 3:
            line.insert(0, EMPTY)
        else:
            line.append(EMPTY)

    return line[:7]


def evaluate_line(line, player):
    """
    Đánh giá một chuỗi 7 ô và trả về điểm số
    """
    # Đếm số quân cùng player trong line (không tính vị trí giữa vì đó là nước đi mới)
    opponent = -player

    # Các pattern cần kiểm tra (line[3] là vị trí đặt quân)
    count = 0
    for i, cell in enumerate(line):
        if cell == player:
            count += 1
        elif cell == opponent:
            return 0  # Bị chặn bởi đối thủ

    # Pattern 4: 3 quân + nước đi = 4 liên tiếp
    if count >= 3:
        return PATTERN_SCORES["four"]

    # Pattern 3: 2 quân + nước đi = 3 liên tiếp
    if count == 2:
        # Kiểm tra xem có bị chặn không
        before = line[0:3].count(player) + line[0:3].count(EMPTY)
        after = line[4:7].count(player) + line[4:7].count(EMPTY)
        if before == 3 and after == 3:
            return PATTERN_SCORES["live_three"]
        else:
            return PATTERN_SCORES["dead_three"]

    # Pattern 2: 1 quân + nước đi = 2 liên tiếp
    if count == 1:
        before_empty = 1 if line[0] == EMPTY else 0
        after_empty = 1 if line[6] == EMPTY else 0
        if before_empty + after_empty >= 1:
            return PATTERN_SCORES["live_two"]
        else:
            return PATTERN_SCORES["dead_two"]

    return 0


def evaluate_board(game, player):
    """
    Đánh giá toàn bộ bàn cờ cho player (PLAYER_X hoặc PLAYER_O)
    Trả về:
    - Điểm dương nếu có lợi cho player
    - Điểm âm nếu có lợi cho đối thủ
    """
    if game.is_terminal():
        result = game.get_result()
        if result == player:
            return 100000  # Thắng
        elif result == -player:
            return -100000  # Thua
        else:
            return 0  # Hòa

    score = 0

    # Duyệt qua tất cả các ô
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if game.board[i][j] == player:
                # Quân của player
                score += evaluate_position(game, i, j, player)
            elif game.board[i][j] == -player:
                # Quân của đối thủ - trừ điểm
                score -= evaluate_position(game, i, j, -player)

    # Bonus cho vị trí trung tâm
    center = BOARD_SIZE // 2
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if game.board[i][j] == player:
                dist_to_center = abs(i - center) + abs(j - center)
                score += max(0, 10 - dist_to_center) * PATTERN_SCORES["center_bonus"]

    return score


def evaluate_simple(game, player):
    """
    Hàm đánh giá đơn giản hơn - đếm các pattern cơ bản
    """
    if game.is_terminal():
        result = game.get_result()
        if result == player:
            return 100000
        elif result == -player:
            return -100000
        else:
            return 0

    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if game.board[i][j] == EMPTY:
                continue

            cell_player = game.board[i][j]
            for d_row, d_col in directions:
                count = 1
                blocked = 0

                # Đếm về phía trước
                r, c = i + d_row, j + d_col
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if game.board[r][c] == cell_player:
                        count += 1
                        r += d_row
                        c += d_col
                    elif game.board[r][c] == -cell_player:
                        blocked += 1
                        break
                    else:
                        break

                # Đếm về phía sau
                r, c = i - d_row, j - d_col
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                    if game.board[r][c] == cell_player:
                        count += 1
                        r -= d_row
                        c -= d_col
                    elif game.board[r][c] == -cell_player:
                        blocked += 1
                        break
                    else:
                        break

                # Tính điểm dựa trên count và blocked
                if count >= 4:
                    pattern_score = 100000
                elif count == 3 and blocked == 0:
                    pattern_score = 1000
                elif count == 3 and blocked == 1:
                    pattern_score = 100
                elif count == 2 and blocked == 0:
                    pattern_score = 100
                elif count == 2 and blocked == 1:
                    pattern_score = 10
                elif count == 1 and blocked == 0:
                    pattern_score = 1
                else:
                    pattern_score = 0

                if cell_player == player:
                    score += pattern_score
                else:
                    score -= pattern_score

    return score


def quick_evaluate(game, player):
    """
    Hàm đánh giá nhanh - chỉ đếm số quân và vị trí
    """
    score = 0
    center = BOARD_SIZE // 2

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if game.board[i][j] == player:
                # Điểm cho mỗi quân
                score += 1
                # Bonus vị trí trung tâm
                dist = abs(i - center) + abs(j - center)
                score += (BOARD_SIZE - dist)
            elif game.board[i][j] == -player:
                score -= 1
                dist = abs(i - center) + abs(j - center)
                score -= (BOARD_SIZE - dist)

    return score
