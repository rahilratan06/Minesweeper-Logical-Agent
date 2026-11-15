import time
import tkinter as tk
from agent import Agent
from game import Minesweeper

BG       = "#b09893"  
TEXT_BG  = "#acd0c7" 
TEXT_FG  = "#0b0c0f"  
BTN_BG   = "#a06f97"  
HIDDEN   = "#dddddd"  
OPEN     = "#B4BCD4"   

NUM_COLORS = {1: "blue", 2: "green", 3: "red", 4: "navy",
              5: "brown", 6: "teal", 7: "black", 8: "gray"}


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        root.title("Minesweeper Logical Agent")
        root.configure(bg=BG)
        self.game = Minesweeper()
        self.agent = Agent(self.game)

        self.board_frame = tk.Frame(root, bg=BG)
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        side = tk.Frame(root, bg=BG)
        side.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        tk.Button(side, text="New Game", width=14, command=self.new_game,
                  bg=BTN_BG, fg="white", activebackground="#1d4ed8",
                  activeforeground="white", relief="flat").pack(pady=2)
        tk.Button(side, text="Agent Step", width=14, command=self.agent_step,
                  bg=BTN_BG, fg="white", activebackground="#1d4ed8",
                  activeforeground="white", relief="flat").pack(pady=2)

        self.status = tk.Label(side, text="Click a cell to start",
                               bg=BG, fg=TEXT_FG)
        self.status.pack(pady=5)

        self.timer_label = tk.Label(side, text="Time: 0.0 s",
                                    font=("Arial", 12, "bold"),
                                    bg=BG, fg=TEXT_FG)
        self.timer_label.pack(pady=2)
        self.start_time = None
        self.elapsed = 0.0

        self.explain = tk.Text(side, width=40, height=18, state="disabled",
                               wrap="word", bg=TEXT_BG, fg=TEXT_FG)
        self.explain.pack()

        self.buttons = {}
        self.build_board()
        self.tick()

    def build_board(self):
        for w in self.board_frame.winfo_children():
            w.destroy()
        self.buttons = {}
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                b = tk.Button(self.board_frame, width=3, height=1,
                              font=("Arial", 12, "bold"), bg=HIDDEN)
                b.grid(row=r, column=c)
                b.bind("<Button-1>", lambda e, r=r, c=c: self.left_click(r, c))
                b.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                self.buttons[(r, c)] = b

    def left_click(self, r, c):
        self.game.reveal(r, c)
        self.refresh()

    def right_click(self, r, c):
        self.game.toggle_flag(r, c)
        self.refresh()

    def refresh(self):
        g = self.game
        if not g.first_click and self.start_time is None:
            self.start_time = time.time()
        if g.game_over and self.start_time is not None:
            self.elapsed = time.time() - self.start_time

        for (r, c), b in self.buttons.items():
            cell = (r, c)
            if cell in g.revealed:
                if cell in g.mines:
                    b.config(text="*", bg="red", fg="black", relief="sunken")
                else:
                    n = g.numbers[cell]
                    b.config(text=str(n) if n else "", relief="sunken",
                             bg=OPEN, fg=NUM_COLORS.get(n, "black"))
            elif g.game_over and cell in g.mines:
                if cell in g.flagged:
                    b.config(text="F", bg="lightgreen", fg="red", relief="sunken")
                else:
                    b.config(text="*", bg="#ff9999", fg="black", relief="sunken")
            elif g.game_over and cell in g.flagged:
                b.config(text="X", bg="yellow", fg="red", relief="sunken")
            elif cell in g.flagged:
                b.config(text="F", fg="red", bg=HIDDEN, relief="raised")
            else:
                b.config(text="", bg=HIDDEN, relief="raised")

        left = g.num_mines - len(g.flagged)
        if g.game_over:
            result = "You won!" if g.won else "Game over! You hit a mine."
            self.status.config(text=f"{result} ({self.elapsed:.1f} s)")
        else:
            self.status.config(text=f"Playing... Mines left: {left}")

    def tick(self):
        if self.start_time is not None and not self.game.game_over:
            self.elapsed = time.time() - self.start_time
        self.timer_label.config(text=f"Time: {self.elapsed:.1f} s")
        self.root.after(100, self.tick)

    def log(self, message):
        self.explain.config(state="normal")
        self.explain.insert("end", message + "\n")
        self.explain.see("end")
        self.explain.config(state="disabled")

    def new_game(self):
        self.game.reset()
        self.start_time = None
        self.elapsed = 0.0
        self.explain.config(state="normal")
        self.explain.delete("1.0", "end")
        self.explain.config(state="disabled")
        self.build_board()
        self.refresh()

    def agent_step(self):
        move = self.agent.step()
        if move is None:
            self.log("Agent has no move (game finished).")
            return
        self.refresh()
        self.log(move["reason"])
        for cell in move["involved"]:
            self.buttons[cell].config(bg="yellow")
        if move["cell"] in self.buttons and move["cell"] not in self.game.revealed:
            self.buttons[move["cell"]].config(bg="orange")