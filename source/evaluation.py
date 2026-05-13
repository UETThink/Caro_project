from source.caro_game import BOARD_SIZE, EMPTY, PLAYER_X, PLAYER_O

PATTERN_SCORES = {
    "four": 10000,
    "live_three": 1000,
    "dead_three": 100,
    "live_two": 100,
    "spread_two": 50,
    "dead_two": 10,
    "center_bonus": 5,
    "adjacent_bonus": 1,
}


def evaluate_position(game, row, col, player):
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for d_row, d_col in directions:
        line = get_line(game, row, col, d_row, d_col, player)
        pattern_score = evaluate_line(line, player)
        score += pattern_score

    return score


def get_line(game, row, col, d_row, d_col, player):
    line = []
    count_before = 0
    count_after = 0

    r, c = row - d_row, col - d_col
    while count_before < 3 and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        line.insert(0, game.board[r][c])
        count_before += 1
        r -= d_row
        c -= d_col

    line.append(player)

    r, c = row + d_row, col + d_col
    while count_after < 3 and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
        line.append(game.board[r][c])
        count_after += 1
        r += d_row
        c += d_col

    while len(line) < 7:
        if len(line) < 3:
            line.insert(0, EMPTY)
        else:
            line.append(EMPTY)

    return line[:7]


def evaluate_line(line, player):
    opponent = -player

    count = 0
    for i, cell in enumerate(line):
        if cell == player:
            count += 1
        elif cell == opponent:
            return 0

    if count >= 3:
        return PATTERN_SCORES["four"]

    if count == 2:
        before = line[0:3].count(player) + line[0:3].count(EMPTY)
        after = line[4:7].count(player) + line[4:7].count(EMPTY)
        if before == 3 and after == 3:
            return PATTERN_SCORES["live_three"]
        else:
            return PATTERN_SCORES["dead_three"]

    if count == 1:
        before_empty = 1 if line[0] == EMPTY else 0
        after_empty = 1 if line[6] == EMPTY else 0
        if before_empty + after_empty >= 1:
            return PATTERN_SCORES["live_two"]
        else:
            return PATTERN_SCORES["dead_two"]

    return 0


def evaluate_board(game, player):
    if game.is_terminal():
        result = game.get_result()
        if result == player:
            return 100000
        elif result == -player:
            return -100000
        else:
            return 0

    score = 0

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if game.board[i][j] == player:
                score += evaluate_position(game, i, j, player)
            elif game.board[i][j] == -player:
                score -= evaluate_position(game, i, j, -player)

    center = BOARD_SIZE // 2
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if game.board[i][j] == player:
                dist_to_center = abs(i - center) + abs(j - center)
                score += max(0, 10 - dist_to_center) * PATTERN_SCORES["center_bonus"]

    return score


def evaluate_simple(game, player):
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
    score = 0
    center = BOARD_SIZE // 2

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if game.board[i][j] == player:
                score += 1
                dist = abs(i - center) + abs(j - center)
                score += (BOARD_SIZE - dist)
            elif game.board[i][j] == -player:
                score -= 1
                dist = abs(i - center) + abs(j - center)
                score -= (BOARD_SIZE - dist)

    return score
