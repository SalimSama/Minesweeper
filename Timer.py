import tkinter as tk
import time
import threading

# Timer-Klasse zur Verwaltung der Zeit während des Spiels
class Timer:
    def __init__(self, master):
        self.master = master
        # Label zur Anzeige der verstrichenen Zeit im Format Stunden:Minuten:Sekunden.Hundertstelsekunden
        self.label = tk.Label(self.master, text="00:00:00.00", font='ariel 15')
        self.label.grid(row=0, column=0, sticky="ew")  # Platzierung des Labels
        self.start_time = None  # Variable zur Speicherung der Startzeit
        self.is_running = False  # Flag, das anzeigt, ob der Timer läuft
        self.keep_running = True  # Flag, um den Timer fortzusetzen oder anzuhalten

    def start(self):
        if not self.is_running:
            # Startet den Timer, wenn er nicht bereits läuft
            self.start_time = time.perf_counter()  # Startzeit wird erfasst
            self.is_running = True
            self.keep_running = True
            self.timer()  # Startet die Aktualisierung des Timers

    def timer(self):
        # Aktualisiert das Timer-Label jede 50 Millisekunden
        if self.keep_running:
            elapsed_time = time.perf_counter() - self.start_time  # Berechnet die verstrichene Zeit
            formatted_time = self.format_time(elapsed_time)  # Formatiert die Zeit für die Anzeige
            self.label.config(text=formatted_time)  # Aktualisiert das Label mit der neuen Zeit
            self.master.after(50, self.timer)  # Ruft die Funktion nach 50 Millisekunden erneut auf

    def stop(self):
        # Stoppt den Timer
        self.is_running = False
        self.keep_running = False

    def reset(self):
        # Setzt den Timer zurück und zeigt wieder 00:00:00.00 an
        self.start_time = None
        self.label.config(text="00:00:00.00")

    @staticmethod
    def format_time(elap):
        # Formatiert die verstrichene Zeit in Stunden:Minuten:Sekunden.Hundertstelsekunden
        hours = int(elap / 3600)
        minutes = int(elap / 60) % 60
        seconds = int(elap) % 60
        mSeconds = int((elap - int(elap)) * 100)
        return f'{hours:02}:{minutes:02}:{seconds:02}.{mSeconds:02}'
