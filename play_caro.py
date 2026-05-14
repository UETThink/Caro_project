# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import tkinter as tk
from tkinter import messagebox

sys.path.insert(0, '..')

from source.caro_game import CaroGame, PLAYER_X, PLAYER_O, BOARD_SIZE


class NeonCaroGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cờ Caro - 9x9")
        self.root.configure(bg="#0a0a1a")
        self.root.resizable(False, False)

        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        display_scale = 0.9

        window_height = int(screen_height * display_scale)
        window_width = int(window_height * display_scale)

        x = (screen_width - window_width) // 2
        y = 0

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.scale = window_height / screen_height

        self.game = None
        self.ai_depth = 3
        self.ai_algorithm = 'alphabeta'
        self.ai_thinking = False
        self.game_started = False

        self.board_size = BOARD_SIZE
        self.cell_size = int(50 * self.scale)
        self.padding = int(10 * self.scale)

        self.neon_blue = "#00d4ff"
        self.neon_red = "#ff0055"
        self.neon_green = "#00ff88"
        self.neon_yellow = "#ffff00"
        self.neon_purple = "#bf00ff"

        self.bg_color = "#0a0a1a"
        self.board_bg = "#ffffff"

        from source.ai_agent import CaroAI
        self.ai = CaroAI(depth=3)

        self.canvas = None

        self.show_menu()

    def show_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(
            menu_frame,
            text="CARO",
            font=("Arial Black", int(80 * self.scale), "bold"),
            fg=self.neon_blue,
            bg=self.bg_color
        )
        title.pack(pady=int(40 * self.scale))

        level_title = tk.Label(
            menu_frame,
            text="Chọn độ khó",
            font=("Arial", int(18 * self.scale), "bold"),
            fg=self.neon_yellow,
            bg=self.bg_color
        )
        level_title.pack(pady=int(15 * self.scale))

        button_frame = tk.Frame(menu_frame, bg=self.bg_color)
        button_frame.pack(pady=int(5 * self.scale))

        self.level_var = tk.StringVar(value="easy")

        btn_height = 2 if self.scale > 0.8 else 1

        easy_btn = tk.Radiobutton(
            button_frame,
            text="Dễ",
            variable=self.level_var,
            value="easy",
            indicatoron=0,
            width=25,
            height=btn_height,
            bg="#1a3a1a",
            fg=self.neon_green,
            selectcolor="#0a4a0a",
            activebackground="#1a3a1a",
            activeforeground=self.neon_green,
            font=("Consolas", int(13 * self.scale), "bold"),
            relief=tk.RAISED,
            bd=3
        )
        easy_btn.pack(pady=int(4 * self.scale))

        medium_btn = tk.Radiobutton(
            button_frame,
            text="Trung bình",
            variable=self.level_var,
            value="medium",
            indicatoron=0,
            width=25,
            height=btn_height,
            bg="#3a3a1a",
            fg=self.neon_yellow,
            selectcolor="#5a5a0a",
            activebackground="#3a3a1a",
            activeforeground=self.neon_yellow,
            font=("Consolas", int(13 * self.scale), "bold"),
            relief=tk.RAISED,
            bd=3
        )
        medium_btn.pack(pady=int(4 * self.scale))

        hard_btn = tk.Radiobutton(
            button_frame,
            text="Khó",
            variable=self.level_var,
            value="hard",
            indicatoron=0,
            width=25,
            height=btn_height,
            bg="#3a1a1a",
            fg=self.neon_red,
            selectcolor="#5a0a0a",
            activebackground="#3a1a1a",
            activeforeground=self.neon_red,
            font=("Consolas", int(13 * self.scale), "bold"),
            relief=tk.RAISED,
            bd=3
        )
        hard_btn.pack(pady=int(4 * self.scale))

        expert_btn = tk.Radiobutton(
            button_frame,
            text="Cực khó",
            variable=self.level_var,
            value="expert",
            indicatoron=0,
            width=25,
            height=btn_height,
            bg="#2a1a3a",
            fg=self.neon_purple,
            selectcolor="#4a2a5a",
            activebackground="#2a1a3a",
            activeforeground=self.neon_purple,
            font=("Consolas", int(13 * self.scale), "bold"),
            relief=tk.RAISED,
            bd=3
        )
        expert_btn.pack(pady=int(4 * self.scale))

        play_btn = tk.Button(
            menu_frame,
            text="BẮT ĐẦU CHƠI",
            command=self.start_game,
            width=20,
            height=btn_height + 1,
            bg=self.neon_blue,
            fg=self.bg_color,
            activebackground=self.neon_green,
            activeforeground=self.bg_color,
            font=("Arial", int(16 * self.scale), "bold"),
            relief=tk.RAISED,
            bd=5,
            cursor="hand2"
        )
        play_btn.pack(pady=int(20 * self.scale))

        info = tk.Label(
            menu_frame,
            text="Bạn: X (Đen) | AI: O (Đỏ) | Thắng: 4 quân liên tiếp",
            font=("Arial", int(9 * self.scale)),
            fg="gray",
            bg=self.bg_color
        )
        info.pack(side=tk.BOTTOM, pady=int(10 * self.scale))

    def start_game(self):
        level = self.level_var.get()

        if level == "easy":
            self.ai_depth = 1
            level_text = "Dễ"
            self.ai_algorithm = 'minimax'

        elif level == "medium":
            self.ai_depth = 2
            level_text = "Trung Bình"
            self.ai_algorithm = 'minimax'

        elif level == "hard":
            self.ai_depth = 3
            level_text = "Khó"
            self.ai_algorithm = 'alphabeta'

        else:
            self.ai_depth = 4
            level_text = "Cực khó"
            self.ai_algorithm = 'alphabeta'

        self.ai.depth = self.ai_depth

        self.game = CaroGame()

        self.game_started = True
        self.ai_thinking = False

        self.show_game_screen(level_text)

    def show_game_screen(self, level_text):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas_size = self.board_size * self.cell_size + self.padding * 2

        self.canvas = tk.Canvas(
            main_frame,
            width=canvas_size,
            height=canvas_size,
            bg=self.board_bg,
            highlightthickness=0,
            cursor="hand2"
        )

        self.canvas.pack(
            side=tk.LEFT,
            padx=int(15 * self.scale),
            pady=int(15 * self.scale)
        )

        control_frame = tk.Frame(main_frame, bg=self.bg_color)

        control_frame.pack(
            side=tk.LEFT,
            padx=int(15 * self.scale),
            pady=int(15 * self.scale),
            fill=tk.BOTH
        )

        title = tk.Label(
            control_frame,
            text="CARO",
            font=("Arial Black", int(26 * self.scale), "bold"),
            fg=self.neon_blue,
            bg=self.bg_color
        )
        title.pack(pady=5)

        level_label = tk.Label(
            control_frame,
            text=f"Cấp độ: {level_text}",
            font=("Arial", int(11 * self.scale)),
            fg=self.neon_purple,
            bg=self.bg_color
        )
        level_label.pack()

        sep = tk.Frame(
            control_frame,
            height=2,
            bg=self.neon_blue,
            width=int(160 * self.scale)
        )
        sep.pack(fill=tk.X, pady=10)

        player_frame = tk.Frame(control_frame, bg=self.bg_color)
        player_frame.pack(pady=5)

        tk.Label(
            player_frame,
            text="BẠN: X",
            font=("Arial", int(13 * self.scale), "bold"),
            fg="#000000",
            bg=self.bg_color
        ).pack()

        tk.Label(
            player_frame,
            text="AI: O",
            font=("Arial", int(13 * self.scale), "bold"),
            fg=self.neon_red,
            bg=self.bg_color
        ).pack()

        sep2 = tk.Frame(
            control_frame,
            height=2,
            bg=self.neon_yellow,
            width=int(160 * self.scale)
        )
        sep2.pack(fill=tk.X, pady=10)

        self.status_label = tk.Label(
            control_frame,
            text="Lượt của bạn",
            font=("Arial", int(15 * self.scale), "bold"),
            fg=self.neon_yellow,
            bg=self.bg_color
        )

        self.status_label.pack(pady=10)

        self.ai_info = tk.Label(
            control_frame,
            text="",
            font=("Courier", int(9 * self.scale)),
            fg="gray",
            bg=self.bg_color,
            justify=tk.LEFT
        )

        self.ai_info.pack(pady=5)

        sep3 = tk.Frame(
            control_frame,
            height=2,
            bg=self.neon_red,
            width=int(160 * self.scale)
        )
        sep3.pack(fill=tk.X, pady=15)

        btn_w = int(14 * self.scale) if self.scale > 0.8 else 12

        menu_btn = tk.Button(
            control_frame,
            text="MENU",
            command=self.back_to_menu,
            width=btn_w,
            height=1 if self.scale < 0.8 else 2,
            bg="#1a1a2e",
            fg=self.neon_yellow,
            activebackground=self.neon_yellow,
            activeforeground=self.bg_color,
            font=("Arial", int(11 * self.scale), "bold"),
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )

        menu_btn.pack(pady=3)

        restart_btn = tk.Button(
            control_frame,
            text="CHƠI LẠI",
            command=self.restart,
            width=btn_w,
            height=1 if self.scale < 0.8 else 2,
            bg="#1a1a2e",
            fg=self.neon_blue,
            activebackground=self.neon_blue,
            activeforeground=self.bg_color,
            font=("Arial", int(11 * self.scale), "bold"),
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )

        restart_btn.pack(pady=3)

        exit_btn = tk.Button(
            control_frame,
            text="THOÁT",
            command=self.root.quit,
            width=btn_w,
            height=1 if self.scale < 0.8 else 2,
            bg="#1a1a2e",
            fg=self.neon_red,
            activebackground=self.neon_red,
            activeforeground=self.bg_color,
            font=("Arial", int(11 * self.scale), "bold"),
            relief=tk.RAISED,
            bd=2,
            cursor="hand2"
        )

        exit_btn.pack(pady=3)

        self.draw_board()

        self.canvas.bind("<Button-1>", self.on_click)

    def back_to_menu(self):
        self.show_menu()

    def draw_board(self):
        self.canvas.delete("all")

        cell = self.cell_size
        size = self.board_size
        padding = self.padding

        start_x = padding
        start_y = padding

        end_x = start_x + size * cell
        end_y = start_y + size * cell

        self.canvas.create_rectangle(
            start_x - 3,
            start_y - 3,
            end_x + 3,
            end_y + 3,
            outline=self.neon_blue,
            width=3
        )

        for col in range(size + 1):
            x = start_x + col * cell

            self.canvas.create_line(
                x,
                start_y,
                x,
                end_y,
                fill="#445566",
                width=1
            )

        for row in range(size + 1):
            y = start_y + row * cell

            self.canvas.create_line(
                start_x,
                y,
                end_x,
                y,
                fill="#445566",
                width=1
            )

    def draw_piece(self, row, col, player):
        cx = self.padding + col * self.cell_size + self.cell_size // 2
        cy = self.padding + row * self.cell_size + self.cell_size // 2

        line_w = max(6, int(8 * self.scale))

        r = self.cell_size // 2 - line_w

        if player == PLAYER_X:
            self.canvas.create_line(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                width=line_w,
                fill="#000000",
                capstyle=tk.ROUND
            )

            self.canvas.create_line(
                cx + r,
                cy - r,
                cx - r,
                cy + r,
                width=line_w,
                fill="#000000",
                capstyle=tk.ROUND
            )

        else:
            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline=self.neon_red,
                width=line_w
            )

    def draw_last_move_indicator(self, row, col):
        cx = self.padding + col * self.cell_size + self.cell_size // 2
        cy = self.padding + row * self.cell_size + self.cell_size // 2

        r = self.cell_size // 2 - 8

        self.canvas.create_oval(
            cx - r,
            cy - r,
            cx + r,
            cy + r,
            outline=self.neon_green,
            width=2,
            dash=(3, 3)
        )

    def on_click(self, event):
        if self.game is None or self.game.game_over or self.ai_thinking:
            return

        if self.game.current_player != PLAYER_X:
            return

        col = int((event.x - self.padding) // self.cell_size)
        row = int((event.y - self.padding) // self.cell_size)

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.game.is_valid_move(row, col):

                self.game.make_move(row, col)

                self.draw_board()
                self.draw_all_pieces()

                self.draw_last_move_indicator(row, col)

                if self.game.is_terminal():
                    self.show_result()
                else:
                    self.ai_turn()

    def draw_all_pieces(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.game.board[i][j] != 0:
                    self.draw_piece(i, j, self.game.board[i][j])

    def ai_turn(self):
        self.ai_thinking = True

        self.status_label.config(
            text="AI ĐANG TÍNH...",
            fg=self.neon_blue
        )

        def ai_move():
            move, score, nodes, elapsed = self.ai.get_best_move(
                self.game,
                self.ai_algorithm
            )

            if move:
                row, col = move

                self.game.make_move(row, col)

                self.draw_board()
                self.draw_all_pieces()

                self.draw_last_move_indicator(row, col)

                self.ai_info.config(
                    text=f"AI: ({row},{col})\n"
                         f"Score: {score}\n"
                         f"Nodes: {nodes}\n"
                         f"Time: {elapsed:.3f}s"
                )

            if self.game.is_terminal():
                self.show_result()
            else:
                self.status_label.config(
                    text="LƯỢT CỦA BẠN",
                    fg=self.neon_yellow
                )

            self.ai_thinking = False

        import threading

        t = threading.Thread(target=ai_move)
        t.start()

    def show_result(self):
        self.game.game_over = True

        result = self.game.get_result()

        if result == PLAYER_X:
            self.status_label.config(
                text="BẠN THẮNG!",
                fg=self.neon_green
            )

            messagebox.showinfo(
                "Kết Quả",
                "Chúc mừng! Bạn đã thắng!"
            )

        elif result == PLAYER_O:
            self.status_label.config(
                text="AI THẮNG!",
                fg=self.neon_red
            )

            messagebox.showinfo(
                "Kết Quả",
                "AI đã thắng! Thật tiếc..."
            )

        else:
            self.status_label.config(
                text="HÒA!",
                fg=self.neon_yellow
            )

            messagebox.showinfo(
                "Kết Quả",
                "Hòa!"
            )

    def restart(self):
        self.game = CaroGame()

        self.ai_info.config(text="")

        self.status_label.config(
            text="LƯỢT CỦA BẠN",
            fg=self.neon_yellow
        )

        self.draw_board()

    def run(self):
        self.root.mainloop()


def main():
    gui = NeonCaroGUI()
    gui.run()

if __name__ == "__main__":
    main()