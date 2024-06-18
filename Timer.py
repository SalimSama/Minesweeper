import tkinter as tk
import time
import threading


class Timer:
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(self.master, text="00:00:00.00", font='ariel 15')
        self.label.grid(row=0, column=0, sticky="ew")
        self.start_time = None
        self.is_running = False
        self.keep_running = True

    def start(self):
        if not self.is_running:
            self.start_time = time.perf_counter()
            self.is_running = True
            self.keep_running = True
            self.timer()

    def timer(self):
        if self.keep_running:
            elapsed_time = time.perf_counter() - self.start_time
            formatted_time = self.format_time(elapsed_time)
            self.label.config(text=formatted_time)
            self.master.after(50, self.timer)

    def stop(self):
        self.is_running = False
        self.keep_running = False

    def reset(self):
        self.start_time = None
        self.label.config(text="00:00:00.00")

    @staticmethod
    def format_time(elap):
        hours = int(elap / 3600)
        minutes = int(elap / 60) % 60
        seconds = int(elap) % 60
        mSeconds = int((elap - int(elap)) * 100)
        return f'{hours:02}:{minutes:02}:{seconds:02}.{mSeconds:02}'
