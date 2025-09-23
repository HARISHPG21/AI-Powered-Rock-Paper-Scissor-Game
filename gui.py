import tkinter as tk
from tkinter import ttk
from ai import RPSAI
import random

class RPSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors Game")
        self.root.geometry("600x720")  # Slightly bigger output screen
        self.theme = "light"
        self.ai = RPSAI()
        self.mode = "AI"
        self.score = {'player1': 0, 'AI': 0, 'player2': 0, 'tie': 0}
        self.history = []
        self.last_result = None
        self.setup_styles()
        self.setup_widgets()

    def setup_styles(self):
        self.styles = {
            "light": {
                "bg": "#f0f0f0", "fg": "#000",
                "button_bg": "#ffffff", "button_fg": "#000",
                "frame_bg": "#e0e0e0",
                "rock_color": "#ffcccb", "paper_color": "#add8e6", "scissors_color": "#d3ffce"
            },
            "dark": {
                "bg": "#2e2e2e", "fg": "#fff",
                "button_bg": "#444", "button_fg": "#fff",
                "frame_bg": "#3c3c3c",
                "rock_color": "#ff4c4c", "paper_color": "#4c9aff", "scissors_color": "#6bff4c"
            }
        }

    def apply_theme(self):
        s = self.styles[self.theme]
        self.root.configure(bg=s['bg'])
        self.top_frame.configure(bg=s['frame_bg'])
        self.label.configure(bg=s['bg'], fg=s['fg'])
        self.result.configure(bg=s['bg'], fg=s['fg'])
        self.ai_strategy.configure(bg=s['bg'], fg=s['fg'])
        self.score_label.configure(bg=s['bg'], fg=s['fg'])
        self.history_label.configure(bg=s['bg'], fg=s['fg'])
        self.bottom_frame.configure(bg=s['frame_bg'])

    def setup_widgets(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)

        self.title_label = tk.Label(self.top_frame, text="Rock-Paper-Scissors Game", font=("Helvetica", 20, "bold"))
        self.title_label.pack()

        self.theme_btn = tk.Button(self.top_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT, padx=10)

        self.mode_btn = tk.Button(self.top_frame, text="Switch to Multiplayer", command=self.toggle_mode)
        self.mode_btn.pack(side=tk.LEFT, padx=10)

        tk.Label(self.top_frame, text="Difficulty:").pack(side=tk.LEFT)
        self.level_var = tk.StringVar(value='Easy')
        self.level_dropdown = ttk.Combobox(self.top_frame, textvariable=self.level_var,
                                           values=['Easy', 'Medium', 'Hard'], state="readonly", width=10)
        self.level_dropdown.pack(side=tk.LEFT)
        self.level_dropdown.bind("<<ComboboxSelected>>", self.set_level)

        self.label = tk.Label(self.root, text="Choose your move:", font=("Helvetica", 14))
        self.label.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.buttons = {}
        emoji_map = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        for move in ['rock', 'paper', 'scissors']:
            btn = tk.Button(self.button_frame, text=emoji_map[move] + " " + move.title(), width=15,
                            height=2, command=lambda m=move: self.play(m))
            btn.pack(side=tk.LEFT, padx=10)
            self.buttons[move] = btn

        self.canvas = tk.Canvas(self.root, width=400, height=200)
        self.canvas.pack(pady=10)

        self.result = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.result.pack(pady=5)

        self.ai_strategy = tk.Label(self.root, text="AI Strategy: Easy", font=("Helvetica", 12))
        self.ai_strategy.pack()

        self.ai_emoji = tk.Label(self.root, text="🤖", font=("Helvetica", 40))
        self.ai_emoji.pack()

        self.score_label = tk.Label(self.root, text="Score: Player1 0 | AI 0 | Player2 0 | Ties 0",
                                    font=("Helvetica", 16, "bold"))
        self.score_label.pack(pady=(10, 5))

        self.history_label = tk.Label(self.root, text="Move History: ", wraplength=600, justify="left",
                                      font=("Helvetica", 14))
        self.history_label.pack(pady=(10, 15))

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(pady=5)

        tk.Button(self.bottom_frame, text="Reset", width=15, height=2, command=self.reset).pack(side=tk.LEFT, padx=10)
        tk.Button(self.bottom_frame, text="Exit", width=15, height=2, command=self.root.quit).pack(side=tk.LEFT, padx=10)

        self.apply_theme()
        self.update_button_colors()

    def update_button_colors(self):
        s = self.styles[self.theme]
        color_map = {
            'rock': s['rock_color'],
            'paper': s['paper_color'],
            'scissors': s['scissors_color']
        }
        for move, btn in self.buttons.items():
            btn.configure(bg=color_map[move], fg=self.styles[self.theme]['fg'])

    def toggle_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.apply_theme()
        self.update_button_colors()

    def toggle_mode(self):
        if self.mode == "AI":
            self.mode = "Multiplayer"
            self.ai_strategy.config(text="Multiplayer Mode")
            self.mode_btn.config(text="Switch to AI")
        else:
            self.mode = "AI"
            self.ai.set_level(self.level_var.get())
            self.ai_strategy.config(text=f"AI Strategy: {self.level_var.get()}")
            self.mode_btn.config(text="Switch to Multiplayer")

    def set_level(self, event=None):
        level = self.level_var.get()
        self.ai.set_level(level)
        self.ai_strategy.config(text=f"AI Strategy: {level}")

    def play(self, player_move):
        self.canvas.delete("all")
        if self.mode == "AI":
            ai_move = self.ai.predict()
            self.last_result = self.calculate_result(player_move, ai_move)
            self.ai.update(player_move)
            self.history.append(f"{player_move} vs {ai_move}")
        else:
            if hasattr(self, 'player1_move'):
                self.player2_move = player_move
                self.last_result = self.calculate_result(self.player1_move, self.player2_move, multiplayer=True)
                self.history.append(f"{self.player1_move} vs {self.player2_move}")
                del self.player1_move
            else:
                self.player1_move = player_move

        self.animate_winner(player_move, ai_move if self.mode == "AI" else self.player2_move)

    def calculate_result(self, player1, player2, multiplayer=False):
        if player1 == player2:
            self.score['tie'] += 1
            return {"text": f"Both chose {player1}. It's a tie!", "winner": "tie", "emoji": "😐"}

        wins = {('rock', 'scissors'), ('paper', 'rock'), ('scissors', 'paper')}
        if (player1, player2) in wins:
            self.score['player1'] += 1
            return {"text": f"Player1 chose {player1}, {('AI' if not multiplayer else 'Player2')} chose {player2}. Player1 wins!", "winner": "player1", "emoji": "😎"}

        if multiplayer:
            self.score['player2'] += 1
            return {"text": f"Player1 chose {player1}, Player2 chose {player2}. Player2 wins!", "winner": "player2", "emoji": "🥳"}
        else:
            self.score['AI'] += 1
            return {"text": f"Player1 chose {player1}, AI chose {player2}. AI wins!", "winner": "AI", "emoji": "🤖"}

    def animate_winner(self, player_move, ai_move):
        self.canvas.create_text(75, 20, text="Player1", font=("Arial", 14))
        self.canvas.create_text(225, 20, text="AI" if self.mode == "AI" else "Player2", font=("Arial", 14))
        self.draw_icon(player_move, 50)
        self.draw_icon(ai_move, 200)
        self.canvas.move("all", random.randint(-10, 10), random.randint(-10, 10))
        self.root.after(700, self.update_display)

    def draw_icon(self, move, x):
        emoji = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}[move]
        self.canvas.create_text(x + 30, 70, text=emoji, font=("Helvetica", 50))

    def update_display(self):
        r = self.last_result
        self.result.config(text=r['text'])
        self.score_label.config(text=f"Score: Player1 {self.score['player1']} | AI {self.score['AI']} | Player2 {self.score['player2']} | Ties {self.score['tie']}")
        self.history_label.config(text="Move History: " + ", ".join(self.history[-10:]))
        self.ai_emoji.config(text=r['emoji'])
        color = {'player1': 'green', 'AI': 'red', 'player2': 'blue', 'tie': 'gray'}[r['winner']]
        self.canvas.create_rectangle(0, 0, 400, 200, outline=color, width=4)

    def reset(self):
        self.ai = RPSAI(level=self.level_var.get())
        self.score = {'player1': 0, 'AI': 0, 'player2': 0, 'tie': 0}
        self.history = []
        self.canvas.delete("all")
        self.ai_emoji.config(text="🤖")
        self.result.config(text="Game reset!")
        self.score_label.config(text="Score: Player1 0 | AI 0 | Player2 0 | Ties 0")
        self.history_label.config(text="Move History: ")

if __name__ == '__main__':
    root = tk.Tk()
    game = RPSGameGUI(root)
    root.mainloop()

