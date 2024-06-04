import tkinter as tk
import time
import threading


class Timer:
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(self.master, text="00:00:00:0", font='ariel 15')
        self.label.pack()
        self.start_time = None
        self.is_running = False
        self.keep_running = True  # Steuerungsflag

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            self.keep_running = True
            self.timer()

    def timer(self):
        if self.keep_running:
            elapsed_time = time.time() - self.start_time
            formatted_time = self.format_time(elapsed_time)
            self.label.config(text=formatted_time)
            self.master.after(50, self.timer)

    def stop(self):
        print("Timer stopping")
        self.keep_running = False  # Setzt das Flag, um den Loop zu beenden
        self.is_running = False

    @staticmethod
    def format_time(elap):
        hours = int(elap / 3600)
        minutes = int(elap / 60 - hours * 60.0)
        seconds = int(elap - hours * 3600.0 - minutes * 60.0)
        mSeconds = int((elap - hours * 3600.0 - minutes * 60.0 - seconds) * 100)
        return '%02d:%02d:%02d.%02d' % (hours, minutes, seconds, mSeconds)
