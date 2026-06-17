# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import time
import math
from source.caro_game import (
    CaroGame, PLAYER_X, PLAYER_O, BOARD_SIZE,
    create_test_state_1, create_test_state_2, create_test_state_3,
    create_test_state_4, create_test_state_5, create_test_state_6
)
from source.ai_agent import CaroAI

def run_full_benchmark():
    test_states = [
        ("State 1 (Empty board)", create_test_state_1()),
        ("State 2 (Mid-game 5 moves)", create_test_state_2()),
        ("State 3 (O has 3 in a row)", create_test_state_3()),
        ("State 4 (X has 3 in a row)", create_test_state_4()),
        ("State 5 (Scattered pieces)", create_test_state_5()),
        ("State 6 (Complex 9 pieces)", create_test_state_6()),
    ]

    depths = [1, 2, 3, 4]

    print("=" * 90)
    print("BENCHMARK: So sánh Minimax và Alpha-Beta Pruning trên các trạng thái thử nghiệm")
    print("=" * 90)

    for state_name, game in test_states:
        print(f"\n{'='*90}")
        print(f"  {state_name}")
        print(f"{'='*90}")
        print(f"  Current player: {'X (PLAYER_X)' if game.current_player == PLAYER_X else 'O (PLAYER_O)'}")
        print(f"  Move count: {game.move_count}")
        game.print_board()

        print(f"  {'Depth':<8} | {'Algorithm':<12} | {'Best Move':<12} | {'Score':<10} | {'Nodes':<10} | {'Time (s)':<12}")
        print(f"  {'-'*8} | {'-'*12} | {'-'*12} | {'-'*10} | {'-'*10} | {'-'*12}")

        for depth in depths:
            # Minimax
            ai_mm = CaroAI(depth=depth)
            game_copy = game.copy()
            try:
                move_mm, score_mm, nodes_mm, time_mm = ai_mm.get_best_move(game_copy, 'minimax')
                move_mm_str = f"({move_mm[0]},{move_mm[1]})" if move_mm else "None"
                print(f"  {depth:<8} | {'Minimax':<12} | {move_mm_str:<12} | {score_mm:<10} | {nodes_mm:<10} | {time_mm:<12.6f}")
            except Exception as e:
                print(f"  {depth:<8} | {'Minimax':<12} | {'TIMEOUT/ERR':<12} | {'-':<10} | {'-':<10} | {'-':<12}")

            # Alpha-Beta
            ai_ab = CaroAI(depth=depth)
            game_copy = game.copy()
            try:
                move_ab, score_ab, nodes_ab, time_ab = ai_ab.get_best_move(game_copy, 'alphabeta')
                move_ab_str = f"({move_ab[0]},{move_ab[1]})" if move_ab else "None"
                print(f"  {depth:<8} | {'Alpha-Beta':<12} | {move_ab_str:<12} | {score_ab:<10} | {nodes_ab:<10} | {time_ab:<12.6f}")
            except Exception as e:
                print(f"  {depth:<8} | {'Alpha-Beta':<12} | {'TIMEOUT/ERR':<12} | {'-':<10} | {'-':<10} | {'-':<12}")

            # Pruning ratio
            try:
                if nodes_ab > 0:
                    ratio = nodes_mm / nodes_ab
                    print(f"  {'':8} | {'-> Ratio':<12} | {'':12} | {'':10} | {f'{ratio:.2f}x':<10} | {f'{time_mm/time_ab:.2f}x' if time_ab > 0 else '-':<12}")
            except:
                pass

        print()

if __name__ == "__main__":
    run_full_benchmark()
