import tkinter as tk
from tkinter import simpledialog, messagebox
from minesweeper import Minesweeper


def start_game(rows, cols, mines, geometry):
    game_window = tk.Tk()
    game_window.title("Minesweeper")
    width, height = map(int, geometry.split('x'))
    center_window(game_window, width, height)
    game = Minesweeper(game_window, rows, cols, mines)
    try:
        menu_window.destroy()
    finally:
        game_window.mainloop()


def show_leaderboard():
    leaderboard_window = tk.Toplevel(menu_window)
    leaderboard_window.title("Top Ranglisten")
    center_window(leaderboard_window, 250, 300)
    leaderboards = Minesweeper.load_leaderboard()
    for difficulty, times in leaderboards.items():
        tk.Label(leaderboard_window,
                 text=f"{difficulty} Bestzeiten: {', '.join([f'{time:.2f}' for time in times])}").pack()


def custom_game():
    custom_window = tk.Toplevel(menu_window)
    custom_window.title("Benutzerdefinierte Einstellungen")
    center_window(custom_window, 150, 200)

    tk.Label(custom_window, text="Reihen (max 30):").pack()
    rows_entry = tk.Entry(custom_window)
    rows_entry.pack()

    tk.Label(custom_window, text="Spalten (max 30):").pack()
    cols_entry = tk.Entry(custom_window)
    cols_entry.pack()

    tk.Label(custom_window, text="Minen (max 800):").pack()
    mines_entry = tk.Entry(custom_window)
    mines_entry.pack()

    def submit_custom():
        try:
            rows = min(30, int(rows_entry.get()))
            cols = min(30, int(cols_entry.get()))
            mines = min(800, int(mines_entry.get()))
            geo_row = int(rows * 31.25)
            geo_col = int(cols * 30)
            geometry = str(geo_row) + "x" + str(geo_col)

        except ValueError:
            messagebox.showerror("Eingabefehler", "Bitte geben Sie gültige Zahlen ein.")
            return

        start_game(rows, cols, mines, geometry)
        custom_window.destroy()  # Zuerst das benutzerdefinierte Fenster schließen
        menu_window.destroy()  # Dann das Hauptmenüfenster schließen

    submit_button = tk.Button(custom_window, text="Spiel starten", command=submit_custom)
    submit_button.pack()


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - width / 2)
    center_y = int(screen_height / 2 - height / 2)
    root.geometry(f'{width}x{height}+{center_x}+{center_y}')


if __name__ == "__main__":
    menu_window = tk.Tk()
    menu_window.title("Minesweeper Menü")
    center_window(menu_window, 250, 250)

    tk.Label(menu_window, text="Minesweeper", font=("Helvetica", 24, "bold")).pack(pady=20)

    tk.Button(menu_window, text="Leicht (8x8, 10 Minen)", command=lambda: start_game(8, 8, 10, '249x210')).pack(
        fill=tk.X)
    tk.Button(menu_window, text="Mittel (16x16, 40 Minen)", command=lambda: start_game(16, 16, 40, '495x420')).pack(
        fill=tk.X)
    tk.Button(menu_window, text="Schwer (30x16, 99 Minen)", command=lambda: start_game(30, 16, 99, '500x780')).pack(
        fill=tk.X)
    tk.Button(menu_window, text="Benutzerdefiniert", command=custom_game).pack(fill=tk.X)
    tk.Button(menu_window, text="Ranglisten anzeigen", command=show_leaderboard).pack(fill=tk.X)
    menu_window.mainloop()
