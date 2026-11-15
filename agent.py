import random


class Agent:
    """Rule-based logical agent. It only uses what a human player can see:
    revealed numbers, flags and hidden cells. Every move comes with a reason."""

    def __init__(self, game):
        self.game = game

    @staticmethod
    def pos(cell):
        """Show cells as (row, col) starting from 1, easier for humans."""
        return f"({cell[0] + 1},{cell[1] + 1})"

    def _constraints(self):
        """Each revealed number gives one constraint:
        'exactly <remaining> of these hidden cells are mines'.
        Returns a list of (source_cell, hidden_cells, remaining_mines)."""
        g = self.game
        constraints = []
        for (r, c) in g.revealed:
            n = g.get_number(r, c)
            if not n:                       
                continue
            nbrs = g.neighbors(r, c)
            flags = [x for x in nbrs if x in g.flagged]
            hidden = frozenset(x for x in nbrs
                               if x not in g.revealed and x not in g.flagged)
            if hidden:
                constraints.append(((r, c), hidden, n - len(flags)))
        return constraints

    @staticmethod
    def _move(action, cell, reason, involved):
        return {"action": action, "cell": cell,
                "reason": reason, "involved": involved}

    def next_move(self):
        g = self.game
        if g.game_over:
            return None

        if g.first_click:
            cell = (g.rows // 2, g.cols // 2)
            return self._move(
                "reveal", cell,
                f"Reveal {self.pos(cell)}: first move, no information yet. "
                f"The first click is always safe.", [])

        constraints = self._constraints()

        for src, hidden, rem in constraints:
            if rem == len(hidden):
                cell = sorted(hidden)[0]
                return self._move(
                    "flag", cell,
                    f"RULE 1 (all mines): cell {self.pos(src)} needs {rem} more "
                    f"mine(s) and has exactly {len(hidden)} hidden neighbour(s), "
                    f"so {self.pos(cell)} must be a mine.", [src])

        for src, hidden, rem in constraints:
            if rem == 0:
                cell = sorted(hidden)[0]
                return self._move(
                    "reveal", cell,
                    f"RULE 2 (all safe): cell {self.pos(src)} already has all "
                    f"its mines flagged, so {self.pos(cell)} is safe.", [src])

        for a_src, a_cells, a_rem in constraints:
            for b_src, b_cells, b_rem in constraints:
                if a_cells < b_cells:
                    diff = b_cells - a_cells
                    diff_rem = b_rem - a_rem
                    if diff_rem == 0:
                        cell = sorted(diff)[0]
                        return self._move(
                            "reveal", cell,
                            f"RULE 3 (subset): hidden cells of {self.pos(a_src)} "
                            f"are inside those of {self.pos(b_src)} and both need "
                            f"the same number of mines, so {self.pos(cell)} is "
                            f"safe.", [a_src, b_src])
                    if diff_rem == len(diff):
                        cell = sorted(diff)[0]
                        return self._move(
                            "flag", cell,
                            f"RULE 3 (subset): subtracting {self.pos(a_src)} from "
                            f"{self.pos(b_src)} leaves {len(diff)} cell(s) that "
                            f"contain {diff_rem} mine(s), so {self.pos(cell)} is "
                            f"a mine.", [a_src, b_src])

        hidden_all = [(r, c) for r in range(g.rows) for c in range(g.cols)
                      if (r, c) not in g.revealed and (r, c) not in g.flagged]
        if not hidden_all:
            return None
        mines_left = g.num_mines - len(g.flagged)
        prob = mines_left / len(hidden_all)
        cell = random.choice(hidden_all)
        return self._move(
            "guess", cell,
            f"GUESS (not a deduction): no rule applies. Overall mine "
            f"probability is about {prob:.0%}. Revealing {self.pos(cell)}.", [])

    def step(self):
        """Choose a move and perform it. Returns the move dict (or None)."""
        move = self.next_move()
        if move is None:
            return None
        r, c = move["cell"]
        if move["action"] == "flag":
            self.game.toggle_flag(r, c)
        else:                                 
            self.game.reveal(r, c)
        return move