import tkinter as tk
from tkinter import simpledialog, messagebox
from minesweeper import Minesweeper


def create_label(window, text, font=None, pack_opts=None):
    label = tk.Label(window, text=text, font=font)
    if pack_opts:
        label.pack(**pack_opts)
    return label


def create_button(window, text, command, pack_opts=None):
    button = tk.Button(window, text=text, command=command)
    if pack_opts:
        button.pack(**pack_opts)
    return button


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
        create_label(leaderboard_window,
                     text=f"{difficulty} Bestzeiten: {', '.join([f'{time:.2f}' for time in times])}",
                     pack_opts={'side': 'top'})


def custom_game():
    custom_window = tk.Toplevel(menu_window)
    custom_window.title("Benutzerdefinierte Einstellungen")
    center_window(custom_window, 150, 200)

    create_label(custom_window, "Reihen (max 30):").pack()
    rows_entry = tk.Entry(custom_window)
    rows_entry.pack()

    create_label(custom_window, "Spalten (max 30):").pack()
    cols_entry = tk.Entry(custom_window)
    cols_entry.pack()

    create_label(custom_window, "Minen (max 800):").pack()
    mines_entry = tk.Entry(custom_window)
    mines_entry.pack()

    def submit_custom():
        try:
            rows = min(30, int(rows_entry.get()))
            cols = min(30, int(cols_entry.get()))
            mines = min(800, int(mines_entry.get()))
            geo_row = int(rows * 31.25)
            geo_col = int(cols * 30)
            geometry = f"{geo_row}x{geo_col}"

        except ValueError:
            messagebox.showerror("Eingabefehler", "Bitte geben Sie gültige Zahlen ein.")
            return

        start_game(rows, cols, mines, geometry)
        custom_window.destroy()
        menu_window.destroy()

    create_button(custom_window, "Spiel starten", submit_custom).pack()


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

    create_label(menu_window, "Minesweeper", font=("Helvetica", 24, "bold"), pack_opts={'pady': 20})
    create_button(menu_window, "Leicht (8x8, 10 Minen)", lambda: start_game(8, 8, 10, '249x210')).pack(fill=tk.X)
    create_button(menu_window, "Mittel (16x16, 40 Minen)", lambda: start_game(16, 16, 40, '495x420')).pack(fill=tk.X)
    create_button(menu_window, "Schwer (30x16, 99 Minen)", lambda: start_game(30, 16, 99, '500x780')).pack(fill=tk.X)
    create_button(menu_window, "Benutzerdefiniert", custom_game).pack(fill=tk.X)
    create_button(menu_window, "Ranglisten anzeigen", show_leaderboard).pack(fill=tk.X)
    menu_window.mainloop()
