# Die Hauptklasse des Programms, darin sind alle Methoden zur Verwaltung des Spiels, sowie hinter der Spiel-Logik
# und die Lösungshilfe

import tkinter as tk
import random
import time
from tkinter import messagebox
import json
from Timer import Timer
import threading


class Minesweeper:
    LEADERBOARD_FILE = "leaderboard.json"  # Datei zum Speichern der Bestzeiten

    def __init__(self, master, rows=7, cols=7, mines=9):
        self.master = master
        # Erstellen eines Frames für den Timer und andere UI-Elemente (z. B. Minenzähler)
        self.timer_frame = tk.Frame(self.master)
        self.timer_frame.grid(row=0, column=0, columnspan=cols, sticky="ew")  # Platzierung des Timer-Frames
        self.timer = Timer(self.timer_frame)  # Initialisierung des Timers im Frame
        self.mines_marked = 0  # Zähler für markierte Minen
        self.marked_label = tk.Label(self.timer_frame, text="Markierte Minen: 0",
                                     font=("Helvetica", 11))  # Label für die Anzeige der markierten Minen
        self.marked_label.grid(row=0, column=cols)  # Platzierung des Labels neben dem Timer
        self.restart_button = tk.Button(self.timer_frame, text="Neustart", font=("Helvetica", 11),
                                        command=self.restart_game)  # Neustart-Button
        self.restart_button.grid(row=0, column=1)
        self.suggestion_button = tk.Button(self.timer_frame, text="Hilfe", font=("Helvetica", 11),
                                           command=self.suggest_move)
        self.suggestion_button.grid(row=0, column=2)  # Platziere den Button neben dem Neustart-Button

        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = []  # Spielbrett zur Speicherung der Minen und Zahlen
        self.mines_location = []  # Liste zur Speicherung der Positionen der Minen
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]  # Matrix für die Buttons im GUI
        self.first_click = True  # Flag zur Überprüfung, ob der erste Klick gemacht wurde
        self.start_time = None  # Startzeit für den Timer
        self.leaderboards = self.load_leaderboard()  # Laden der bisherigen Bestzeiten aus der Datei
        self.init_board()  # Initialisierung des Spielfeldes (Erstellen der Buttons)

    @staticmethod
    def load_leaderboard():
        try:
            with open(Minesweeper.LEADERBOARD_FILE, 'r') as file:
                return json.load(file)  # Laden der Ranglisten aus der JSON-Datei
        except FileNotFoundError:
            return {}  # Falls die Datei nicht existiert, eine leere Rangliste zurückgeben

    @staticmethod
    def save_leaderboard(leaderboards):
        with open(Minesweeper.LEADERBOARD_FILE, 'w') as file:
            json.dump(leaderboards, file)  # Speichern der aktualisierten Ranglisten in der JSON-Datei

    def update_leaderboard(self, new_time):
        # Aktualisierung der Rangliste mit der neuen Spielzeit
        difficulty = f"Spiel: {self.rows}x{self.cols} mit {self.mines} Minen"
        if difficulty not in self.leaderboards:
            self.leaderboards[difficulty] = []
        self.leaderboards[difficulty].append(new_time)
        self.leaderboards[difficulty] = sorted(self.leaderboards[difficulty])[:5]  # Nur die besten 5 Zeiten speichern
        self.save_leaderboard(self.leaderboards)

    def init_board(self):
        # Initialisierung des Spielfeldes durch Erstellen von Buttons für jedes Feld
        for row in range(self.rows):
            self.master.grid_rowconfigure(row + 1, minsize=30, weight=1)
            for col in range(self.cols):
                self.master.grid_columnconfigure(col, minsize=30, weight=1)
                button = tk.Button(self.master, text=' ', font=("Helvetica", 9, "bold"),
                                   command=lambda r=row, c=col: self.reveal_tile(r, c))
                button.bind("<Button-3>",
                            lambda e, r=row, c=col: self.mark_mine(r, c))  # Rechtsklick zum Markieren einer Mine
                button.grid(row=row + 1, column=col,
                            sticky="nsew")  # Positionierung der Buttons (Zeilenversatz für den Timer)
                self.buttons[row][col] = button  # Speichern der Buttons in der Matrix

    def place_mines(self, start_row, start_col):
        # Platzierung der Minen auf dem Spielfeld
        count = 0
        while count < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            # Vermeidung, dass die erste aufgedeckte Stelle eine Mine ist und keine doppelte Minenplatzierung
            if (row, col) != (start_row, start_col) and (row, col) not in self.mines_location:
                self.mines_location.append((row, col))  # Hinzufügen der Mine zur Liste
                count += 1
        self.update_numbers()  # Aktualisierung der Zahlen auf den Feldern basierend auf der Minenplatzierung

    def update_numbers(self):
        # Berechnung der Zahlen für jedes Feld basierend auf den angrenzenden Minen
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.mines_location:
                    continue  # Falls das Feld eine Mine ist, keine Zahl berechnen
                count = sum(
                    (nr, nc) in self.mines_location
                    for nr in range(row - 1, row + 2)
                    for nc in range(col - 1, col + 2)
                    if 0 <= nr < self.rows and 0 <= nc < self.cols)
                self.board.append((row, col, count))  # Speichern der berechneten Zahl im Spielbrett

    def reveal_tile(self, row, col):
        # Aufdecken eines Feldes, wenn darauf geklickt wird
        if self.buttons[row][col].cget('text') == 'M':
            self.mines_marked -= 1  # Falls es vorher als Mine markiert war, die Markierung zurücksetzen
            self.marked_label.config(text=f"Markierte Minen: {self.mines_marked}")
        if self.first_click:
            # Wenn es der erste Klick ist, Minen platzieren und den Timer starten
            self.first_click = False
            self.start_time = time.time()
            threading.Thread(target=self.timer.start).start()  # Starten des Timers in einem separaten Thread
            self.place_mines(row, col)  # Platzieren der Minen, ohne die erste geklickte Stelle zu belegen
        if (row, col) in self.mines_location:
            # Falls eine Mine aufgedeckt wird, das Spiel beenden und alle Felder aufdecken
            self.buttons[row][col].config(text='*', bg='red')
            self.reveal_all()
            for r in range(self.rows):
                for c in range(self.cols):
                    self.buttons[r][c]['state'] = 'disabled'  # Deaktivieren aller Buttons nach Spielende
            self.timer.stop()  # Timer stoppen
            messagebox.showinfo("Game Over", "Sie haben eine Mine erwischt!")  # Anzeige einer Spielende-Nachricht
            return
        else:
            # Falls das aufgedeckte Feld keine Mine enthält, die entsprechende Zahl anzeigen
            num_mines = self.get_mine_count(row, col)
            self.buttons[row][col]['state'] = 'disabled'
            self.buttons[row][col].config(text=str(num_mines), bg='white')

            if num_mines == 0:
                self.reveal_neighbors(row,
                                      col)  # Automatisches Aufdecken der angrenzenden Felder, falls keine Minen angrenzen
        if self.check_win():
            # Überprüfen, ob das Spiel gewonnen wurde
            self.timer.stop()  # Timer stoppen
            messagebox.showinfo("Glückwunsch!", "Sie haben das Spiel gewonnen!")  # Gewinn-Nachricht anzeigen
            for r in range(self.rows):
                for c in range(self.cols):
                    self.buttons[r][c]['state'] = 'disabled'  # Deaktivieren aller Buttons nach dem Gewinn

    def mark_mine(self, row, col):
        # Markieren eines Feldes als Mine oder als unsicher (Fragezeichen)
        if self.buttons[row][col]['state'] != 'disabled':
            current_text = self.buttons[row][col]['text']
            if current_text == ' ':
                self.buttons[row][col].config(text='M', bg='orange')
                self.mines_marked += 1
            elif current_text == 'M':
                self.buttons[row][col].config(text='?', bg='yellow')
                self.mines_marked -= 1
            else:
                self.buttons[row][col].config(text=' ', bg='SystemButtonFace')

        self.marked_label.config(text=f"Markierte Minen: {self.mines_marked}")

    def reveal_neighbors(self, row, col):
        # Automatisches Aufdecken der angrenzenden Felder, falls das aktuelle Feld keine angrenzenden Minen hat
        for nr in range(row - 1, row + 2):
            for nc in range(col - 1, col + 2):
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.buttons[nr][nc]['text'] == ' ':
                    self.reveal_tile(nr, nc)  # Rekursives Aufdecken der Nachbarfelder

    def check_win(self):
        # Überprüfen, ob alle Nicht-Minen-Felder aufgedeckt wurden
        revealed_count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                button = self.buttons[row][col]
                if button['text'] != ' ' and (row, col) not in self.mines_location:
                    revealed_count += 1

        # Die Anzahl der Nicht-Minen-Felder ist die Gesamtzahl der Felder minus die Anzahl der Minen
        total_non_mines = self.rows * self.cols - self.mines
        if revealed_count == total_non_mines:
            elapsed_time = time.time() - self.start_time  # Berechnung der vergangenen Zeit
            self.update_leaderboard(elapsed_time)  # Aktualisierung der Rangliste mit der neuen Bestzeit
            return True  # Spiel gewonnen
        return False  # Spiel noch nicht gewonnen

    def get_mine_count(self, row, col):
        # Zählt die Anzahl der Minen in den benachbarten Feldern um das Feld (row, col)
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if (r, c) in self.mines_location:
                    count += 1
        return count

    def reveal_all(self):
        # Aufdecken aller Felder, um das Spielende anzuzeigen (nach Gewinn oder Verlust)
        updates = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mines_location:
                    updates.append((r, c, '*', 'red'))  # Anzeige einer Mine
                else:
                    num_mines = self.get_mine_count(r, c)
                    updates.append((r, c, str(num_mines), 'white'))  # Anzeige der Anzahl der angrenzenden Minen
                    if num_mines == 0:
                        self.reveal_neighbors(r, c)  # Rekursives Aufdecken von benachbarten Feldern

        for r, c, text, bg in updates:
            self.buttons[r][c].config(text=text, bg=bg)  # Aktualisierung der Anzeige der Buttons

    def get_neighbors(self, r, c):
        #Name der Methode erklärt sie bereits
        #um ein Feld werden die 8 Nachbarn zurückgegeben
        neighbors = []
        for i in range(max(0, r - 1), min(self.rows, r + 2)):
            for j in range(max(0, c - 1), min(self.cols, c + 2)):
                if (i, j) != (r, c):
                    neighbors.append((i, j))
        return neighbors

    def find_safe_move(self):
        # Diese Methode sucht nach sicheren Zügen, indem sie Felder analysiert, die
        # bereits aufgedeckt wurden und ihre Nachbarn bewertet.
        known_mines = set()  # Set für bekannte Minen, die sicher markiert sind
        safe_moves = set()  # Set für sichere Züge, die aufgedeckt werden können

        for r in range(self.rows):
            for c in range(self.cols):
                button_text = self.buttons[r][c].cget('text')  # Text des Buttons abfragen
                if button_text.isdigit():  # Falls das Feld eine Zahl zeigt
                    num_mines = int(button_text)  # Anzahl der Minen, die das Feld umgeben
                    neighbors = self.get_neighbors(r, c)  # Nachbarfelder des aktuellen Felds abfragen
                    hidden_neighbors = [(i, j) for i, j in neighbors if self.buttons[i][j].cget(
                        'text') == ' ']  # Nachbarfelder, die noch nicht aufgedeckt wurden
                    marked_neighbors = [(i, j) for i, j in neighbors if self.buttons[i][j].cget(
                        'text') == 'M']  # Nachbarfelder, die als Minen markiert wurden

                    if len(marked_neighbors) == num_mines:
                        # Wenn alle Minen in den Nachbarfeldern markiert sind, können alle
                        # anderen Felder als sicher angesehen werden
                        for n in hidden_neighbors:
                            if n not in known_mines:
                                safe_moves.add(n)  # Sichere Züge hinzufügen

                    if len(hidden_neighbors) == num_mines - len(marked_neighbors):
                        # Wenn die Anzahl der versteckten Nachbarfelder der Anzahl der verbleibenden
                        # unmarkierten Minen entspricht, diese Nachbarn als Minen markieren
                        for n in hidden_neighbors:
                            known_mines.add(n)  # Feld als Mine markieren
                            self.mark_mine(n[0], n[1])  # Minen-Flag setzen

        if safe_moves:
            return safe_moves.pop()  # Sicheres Feld zurückgeben
        else:
            return None  # Kein sicherer Zug gefunden

    def suggest_move(self):
        # Diese Methode schlägt einen sicheren Zug vor (basierend auf seine Moves) oder fragt den Spieler, ob er
        # ein Risiko eingehen und raten möchte.
        move = self.find_safe_move()  # Sicheren Zug suchen
        if move:
            row, col = move
            self.mark(row, col)  # Sicheres Feld aufdecken
        else:
            # Wenn kein sicherer Zug gefunden wird, wird der Spieler gefragt, ob er raten möchte
            response = messagebox.askyesno("Raten?", "Kein sicherer Zug gefunden. Soll ich raten?")
            if response:
                self.random_guess()  # Zufälliges Feld aufdecken

    def random_guess(self):
        # Diese Methode wählt zufällig ein verdecktes Feld aus und deckt es auf, wenn kein sicherer Zug verfügbar ist
        hidden_tiles = [(r, c) for r in range(self.rows) for c in range(self.cols) if
                        self.buttons[r][c].cget('text') == ' ']  # Alle verdeckten Felder sammeln
        if hidden_tiles:
            row, col = random.choice(hidden_tiles)  # Zufälliges verdecktes Feld wählen
            self.reveal_tile(row, col)  # Gewähltes Feld aufdecken

    def restart_game(self):
        # Neustart des Spiels: Zurücksetzen aller Felder und Timer
        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col].config(text=' ', bg='SystemButtonFace',
                                              state='normal')  # Zurücksetzen der Felder
        self.mines_location.clear()  # Löschen der Minenliste
        self.board.clear()  # Löschen des Spielbretts
        self.first_click = True  # Zurücksetzen des ersten Klicks
        self.mines_marked = 0  # Zurücksetzen des Minenzählers
        self.marked_label.config(text="Markierte Minen: 0")  # Zurücksetzen des Labels
        self.timer.stop()  # Timer stoppen
        self.timer.reset()  # Timer zurücksetzen

    def mark(self, row, col):
        self.buttons[row][col].config(text=' ', bg='green')


