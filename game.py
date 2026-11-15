import random


class Minesweeper:
    """Game engine: board, mines, reveal logic. No AI here."""

    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.num_mines = mines
        self.reset()

    def reset(self):
        """Start a fresh game. Mines are placed on the first click."""
        self.mines = set()                 
        self.revealed = set()              
        self.flagged = set()               
        self.numbers = {}                  
        self.first_click = True
        self.game_over = False
        self.won = False

    def neighbors(self, r, c):
        """Return the up-to-8 cells around (r, c) that are inside the board."""
        result = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    result.append((nr, nc))
        return result

    def _place_mines(self, safe_r, safe_c):
        """Place mines randomly, keeping the first-clicked cell and its
        neighbours mine-free, so the first click is always safe."""
        forbidden = set(self.neighbors(safe_r, safe_c)) | {(safe_r, safe_c)}
        candidates = [(r, c) for r in range(self.rows)
                      for c in range(self.cols) if (r, c) not in forbidden]
        self.mines = set(random.sample(candidates, self.num_mines))

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mines:
                    self.numbers[(r, c)] = sum(
                        1 for n in self.neighbors(r, c) if n in self.mines)

    def reveal(self, r, c):
        """Open a cell. Returns the list of cells that got revealed."""
        if self.game_over or (r, c) in self.revealed or (r, c) in self.flagged:
            return []

        if self.first_click:
            self._place_mines(r, c)
            self.first_click = False

        if (r, c) in self.mines:
            self.game_over = True
            self.revealed.add((r, c))
            return [(r, c)]

        opened = []
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if (cr, cc) in self.revealed or (cr, cc) in self.flagged:
                continue
            self.revealed.add((cr, cc))
            opened.append((cr, cc))
            if self.numbers[(cr, cc)] == 0:
                stack.extend(self.neighbors(cr, cc))

        self._check_win()
        return opened

    def toggle_flag(self, r, c):
        """Place or remove a flag on an unrevealed cell."""
        if self.game_over or (r, c) in self.revealed:
            return
        if (r, c) in self.flagged:
            self.flagged.remove((r, c))
        else:
            self.flagged.add((r, c))

    def _check_win(self):
        """Win when every non-mine cell has been revealed."""
        if len(self.revealed) == self.rows * self.cols - self.num_mines:
            self.won = True
            self.game_over = True

    def get_number(self, r, c):
        """What the player can see: number if revealed, else None."""
        if (r, c) in self.revealed and (r, c) not in self.mines:
            return self.numbers[(r, c)]
        return None