import math
import time
from source.caro_game import CaroGame, PLAYER_X, PLAYER_O
from source.evaluation import evaluate_board, evaluate_simple, quick_evaluate


class CaroAI:
    def __init__(self, depth=3, evaluation_func=None):
        self.depth = depth
        self.evaluation_func = evaluation_func if evaluation_func else evaluate_simple
        self.nodes_visited = 0
        self.best_move = None
        self.best_value = None

    def reset_stats(self):
        self.nodes_visited = 0
        self.best_move = None
        self.best_value = None

    def get_best_move(self, game, algorithm='minimax', use_bound=True):
        self.reset_stats()
        start_time = time.time()

        valid_moves = game.get_valid_moves() if use_bound else game.get_all_valid_moves()

        if not valid_moves:
            return None, None, 0, time.time() - start_time

        if algorithm == 'minimax':
            best_score = -math.inf
            best_move = None

            for move in valid_moves:
                row, col = move
                game_copy = game.copy()
                game_copy.make_move(row, col)

                self.nodes_visited += 1
                score = self.minimax(game_copy, self.depth - 1, False)

                if score > best_score:
                    best_score = score
                    best_move = move

            self.best_move = best_move
            self.best_value = best_score

        elif algorithm == 'alphabeta':
            best_score = -math.inf
            best_move = None
            alpha = -math.inf
            beta = math.inf

            for move in valid_moves:
                row, col = move
                game_copy = game.copy()
                game_copy.make_move(row, col)

                self.nodes_visited += 1
                score = self.alpha_beta(game_copy, self.depth - 1, alpha, beta, False)

                if score > best_score:
                    best_score = score
                    best_move = move
                    alpha = max(alpha, score)

            self.best_move = best_move
            self.best_value = best_score

        elapsed_time = time.time() - start_time

        return self.best_move, self.best_value, self.nodes_visited, elapsed_time

    def minimax(self, game, depth, is_maximizing):
        self.nodes_visited += 1

        if game.is_terminal():
            result = game.get_result()
            if result == PLAYER_O:
                return 100000
            elif result == PLAYER_X:
                return -100000
            else:
                return 0

        if depth == 0:
            return self.evaluation_func(game, PLAYER_O)

        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return 0

        if is_maximizing:
            max_val = -math.inf
            for move in valid_moves:
                row, col = move
                game_copy = game.copy()
                game_copy.make_move(row, col)
                val = self.minimax(game_copy, depth - 1, False)
                max_val = max(max_val, val)
            return max_val
        else:
            min_val = math.inf
            for move in valid_moves:
                row, col = move
                game_copy = game.copy()
                game_copy.make_move(row, col)
                val = self.minimax(game_copy, depth - 1, True)
                min_val = min(min_val, val)
            return min_val

    def alpha_beta(self, game, depth, alpha, beta, is_maximizing):
        self.nodes_visited += 1

        if game.is_terminal():
            result = game.get_result()
            if result == PLAYER_O:
                return 100000
            elif result == PLAYER_X:
                return -100000
            else:
                return 0

        if depth == 0:
            return self.evaluation_func(game, PLAYER_O)

        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return 0

        if is_maximizing:
            max_val = -math.inf
            for move in valid_moves:
                row, col = move
                game_copy = game.copy()
                game_copy.make_move(row, col)
                val = self.alpha_beta(game_copy, depth - 1, alpha, beta, False)
                max_val = max(max_val, val)
                alpha = max(alpha, val)

                if beta <= alpha:
                    break
            return max_val
        else:
            min_val = math.inf
            for move in valid_moves:
                row, col = move
                game_copy = game.copy()
                game_copy.make_move(row, col)
                val = self.alpha_beta(game_copy, depth - 1, alpha, beta, True)
                min_val = min(min_val, val)
                beta = min(beta, val)

                if beta <= alpha:
                    break
            return min_val

    def minimax_with_pruning_stats(self, game, depth, is_maximizing):
        self.nodes_visited += 1

        if game.is_terminal():
            result = game.get_result()
            if result == PLAYER_O:
                return 100000
            elif result == PLAYER_X:
                return -100000
            else:
                return 0

        if depth == 0:
            return self.evaluation_func(game, PLAYER_O)

        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return 0

        if is_maximizing:
            max_val = -math.inf
            for move in valid_moves:
                row, col = move
                game_copy = game.copy()
                game_copy.make_move(row, col)
                val = self.minimax_with_pruning_stats(game_copy, depth - 1, False)
                max_val = max(max_val, val)
            return max_val
        else:
            min_val = math.inf
            for move in valid_moves:
                row, col = move
                game_copy = game.copy()
                game_copy.make_move(row, col)
                val = self.minimax_with_pruning_stats(game_copy, depth - 1, True)
                min_val = min(min_val, val)
            return min_val

    def compare_algorithms(self, game, depths=[1, 2, 3]):
        results = []

        for depth in depths:
            self.depth = depth

            self.reset_stats()
            start_time = time.time()
            minimax_game = game.copy()
            _, minimax_score, minimax_nodes, _ = self.get_best_move(minimax_game, 'minimax')
            minimax_time = time.time() - start_time

            self.reset_stats()
            alphabeta_game = game.copy()
            _, alphabeta_score, alphabeta_nodes, _ = self.get_best_move(alphabeta_game, 'alphabeta')
            alphabeta_time = time.time() - start_time

            results.append({
                'depth': depth,
                'minimax': {
                    'score': minimax_score,
                    'nodes': minimax_nodes,
                    'time': minimax_time
                },
                'alphabeta': {
                    'score': alphabeta_score,
                    'nodes': alphabeta_nodes,
                    'time': alphabeta_time
                },
                'pruning_ratio': minimax_nodes / alphabeta_nodes if alphabeta_nodes > 0 else 0,
                'same_move': True
            })

        return results


def run_benchmark(game, depths=[1, 2, 3]):
    print("=" * 70)
    print("BENCHMARK: So sánh Minimax và Alpha-Beta Pruning")
    print("=" * 70)
    print(f"\nTrạng thái bàn cờ ban đầu:")
    game.print_board()
    print("-" * 70)

    results_table = []

    for depth in depths:
        print(f"\n>>> Độ sâu = {depth}")

        ai_minimax = CaroAI(depth=depth)
        _, score_minimax, nodes_minimax, time_minimax = ai_minimax.get_best_move(
            game.copy(), 'minimax'
        )

        ai_alphabeta = CaroAI(depth=depth)
        move_ab, score_ab, nodes_ab, time_ab = ai_alphabeta.get_best_move(
            game.copy(), 'alphabeta'
        )

        pruning_ratio = nodes_minimax / nodes_ab if nodes_ab > 0 else 0
        time_ratio = time_minimax / time_ab if time_ab > 0 else 0

        print(f"  MINIMAX:    Score={score_minimax:8d} | Nodes={nodes_minimax:6d} | Time={time_minimax:.4f}s")
        print(f"  ALPHA-BETA: Score={score_ab:8d} | Nodes={nodes_ab:6d} | Time={time_ab:.4f}s")
        print(f"  -> Alpha-Beta cắt bỏ {pruning_ratio:.2f}x trạng thái | Tốc độ nhanh hơn {time_ratio:.2f}x")

        results_table.append({
            'depth': depth,
            'minimax_nodes': nodes_minimax,
            'alphabeta_nodes': nodes_ab,
            'pruning_effect': f"{pruning_ratio:.2f}x"
        })

    return results_table


if __name__ == "__main__":
    from source.caro_game import create_test_state_2

    game = create_test_state_2()
    game.print_board()

    results = run_benchmark(game, depths=[1, 2, 3])
