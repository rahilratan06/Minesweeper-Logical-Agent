# Minesweeper Logical Agent

An AI agent that plays Minesweeper using logical deduction and explains every move.
Course project for Artificial Intelligence (INT3120), Manipal University Jaipur.

## Description
The agent treats each revealed number as a constraint on its hidden neighbours
(a Constraint Satisfaction model) and applies rule-based inference to find cells
that are certainly mines or certainly safe. Each move is shown with a reason in
the GUI, and the cells used as evidence are highlighted. If no rule applies, the
agent makes a random guess and labels it as a guess.

## Features
- 9x9 board with 10 mines and a guaranteed safe first click
- Manual play: left-click to reveal, right-click to flag
- Agent Step button: the agent makes one move with an explanation
- Three inference rules: all-mines, all-safe, subset rule
- Evidence cells in yellow, target cell in orange
- Mines-left counter and game timer
- All mines revealed when the game ends

## Requirements
- Python 3.8 or higher
- Tkinter (included with Python on Windows and macOS)
- On Linux: `sudo apt install python3-tk`
- No other packages are needed

## How to Run
1. Download or clone this repository:
   `git clone https://github.com/rahilratan06/Minesweeper-Logical-Agent.git`
2. Open the folder in a terminal.
3. Run:
   `python main.py`

## How to Use
- Click any cell to start. The first click is always safe.
- Press **Agent Step** to let the agent make one move. Read the reason in the panel.
- Right-click a cell to place or remove a flag.
- Press **New Game** to restart.

## Project Structure
- `game.py`: board, mines, reveal logic, flood-fill
- `agent.py`: constraints, inference rules, explanations
- `gui.py`: Tkinter interface, timer, explanation panel
- `main.py`: entry point

## Author
Rahil Ratan, 2430030229