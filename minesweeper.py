import tkinter as tk
import random
import time
from tkinter import messagebox
import json
from Timer import Timer
import threading


class Minesweeper:
    LEADERBOARD_FILE = "leaderboard.json"

    def __init__(self, master, rows=7, cols=7, mines=9):
        self.master = master
        # Erstellen eines Frames für den Timer
        self.timer_frame = tk.Frame(self.master)
        self.timer_frame.grid(row=0, column=0, columnspan=cols, sticky="ew")  # Sticky "ew" dehnt den Frame horizontal
        self.timer = Timer(self.timer_frame)  # Timer im Frame initialisieren

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = []
        self.mines_location = []
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.first_click = True
        self.start_time = None
        self.leaderboards = self.load_leaderboard()
        self.init_board()

    @staticmethod
    def load_leaderboard():
        try:
            with open(Minesweeper.LEADERBOARD_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_leaderboard(leaderboards):
        with open(Minesweeper.LEADERBOARD_FILE, 'w') as file:
            json.dump(leaderboards, file)

    def update_leaderboard(self, new_time):
        difficulty = f"{self.rows}x{self.cols}-{self.mines}"
        if difficulty not in self.leaderboards:
            self.leaderboards[difficulty] = []
        self.leaderboards[difficulty].append(new_time)
        self.leaderboards[difficulty] = sorted(self.leaderboards[difficulty])[:5]
        self.save_leaderboard(self.leaderboards)

    def init_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.master, text=' ', width=3, command=lambda r=row, c=col: self.reveal_tile(r, c))
                button.bind("<Button-3>", lambda e, r=row, c=col: self.mark_mine(r, c))
                button.grid(row=row + 1, column=col)  # Achtung: Startet bei row+1, um Platz für den Timer zu machen
                self.buttons[row][col] = button

    def place_mines(self, start_row, start_col):
        count = 0
        while count < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) != (start_row, start_col) and (row, col) not in self.mines_location:
                self.mines_location.append((row, col))
                count += 1
        self.update_numbers()

    def update_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.mines_location:
                    continue
                count = sum(
                    (nr, nc) in self.mines_location
                    for nr in range(row - 1, row + 2)
                    for nc in range(col - 1, col + 2)
                    if 0 <= nr < self.rows and 0 <= nc < self.cols)
                self.board.append((row, col, count))

    def reveal_tile(self, row, col):
        if self.first_click:
            self.first_click = False
            threading.Thread(target=self.timer.start).start()  # Timer starten in einem Thread
            self.place_mines(row, col)
        if (row, col) in self.mines_location:
            self.buttons[row][col].config(text='*', bg='red')
            for r in range(self.rows):
                for c in range(self.cols):
                    self.reveal_all()
                    self.buttons[r][c]['state'] = 'disabled'
                    self.timer.stop()  # Timer stoppen, wenn das Spiel verloren ist
            messagebox.showinfo("Game Over", "You hit a mine!")
            self.master.destroy()
        else:
            num_mines = self.get_mine_count(row, col)
            self.buttons[row][col].config(text=str(num_mines), bg='white')
            if num_mines == 0:
                self.reveal_neighbors(row, col)
        if self.check_win():
            self.timer.stop()  # Timer stoppen, wenn das Spiel gewonnen ist
            for r in range(self.rows):
                for c in range(self.cols):
                    self.buttons[r][c]['state'] = 'disabled'  # Deaktiviere alle Buttons nach dem Gewinn

    def mark_mine(self, row, col):
        current_text = self.buttons[row][col]['text']
        if current_text == ' ':
            self.buttons[row][col].config(text='M', bg='orange')
        elif current_text == 'M':
            self.buttons[row][col].config(text='?', bg='yellow')
        else:
            self.buttons[row][col].config(text=' ', bg='SystemButtonFace')

    def reveal_neighbors(self, row, col):
        for nr in range(row - 1, row + 2):
            for nc in range(col - 1, col + 2):
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.buttons[nr][nc]['text'] == ' ':
                    self.reveal_tile(nr, nc)

    def check_win(self):
        # Zähle die Anzahl der aufgedeckten Felder
        revealed_count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                button = self.buttons[row][col]
                if button['text'] != ' ' and (row, col) not in self.mines_location:
                    revealed_count += 1

        # Die Anzahl der Nicht-Minen-Felder ist Gesamtzahl der Felder minus die Anzahl der Minen
        total_non_mines = self.rows * self.cols - self.mines
        if revealed_count == total_non_mines:
            elapsed_time = time.time() - self.start_time
            self.update_leaderboard(elapsed_time)
            # Alle Nicht-Minen-Felder wurden aufgedeckt
            messagebox.showinfo("Glückwunsch!", "Sie haben das Spiel gewonnen!")
            return True
        return False

    def get_mine_count(self, row, col):
        # Zählt die Anzahl der Minen in den benachbarten Feldern um das Feld (row, col)
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if (r, c) in self.mines_location:
                    count += 1
        return count

    def reveal_all(self):  #muss noch omptimiert werden
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mines_location:
                    self.buttons[r][c].config(text='*', bg='red')
                else:

                    num_mines = self.get_mine_count(r, c)
                    self.buttons[r][c].config(text=str(num_mines), bg='white')
                    if num_mines == 0:
                        self.reveal_neighbors(r, c)
