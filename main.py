# Startet das Programm und öffnet das Menü, bekommt als Eingabe die gewünschten Spieleinstellungen
import tkinter as tk
from tkinter import messagebox
from minesweeper import Minesweeper


# Funktion zur Erstellung eines Labels mit bestimmten Eigenschaften
def create_label(window, text, font=None, pack_opts=None):
    label = tk.Label(window, text=text, font=font, bg="#1c1c1c", fg="#ffffff", bd=7)  # Hintergrund und Schriftfarbe
    label.pack(padx=20, pady=20)
    if pack_opts:
        label.pack(**pack_opts)  # Platzierung des Labels im Fenster
    return label


# Funktion zur Erstellung eines Buttons mit bestimmten Eigenschaften
def create_button(window, text, command, pack_opts=None):
    button = tk.Button(window, text=text, font=("Helvetica", 16, "bold"), command=command, width=19, height=1,
                       bg="#005f99", fg="#ffffff", relief=tk.FLAT, bd=10)
    button.pack(padx=20, pady=7, anchor='w')
    if pack_opts:
        button.pack(**pack_opts)

    # Hinzufügen eines Hover-Effekts, um die Benutzererfahrung zu verbessern
    def on_enter(e):
        button['bg'] = '#007acc'  # Farbe ändern, wenn die Maus über dem Button ist

    def on_leave(e):
        button['bg'] = '#005f99'  # Farbe zurücksetzen, wenn die Maus den Button verlässt

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button


# Startet das Minesweeper-Spiel mit den angegebenen Einstellungen
def start_game(rows, cols, mines, geometry):
    game_window = tk.Tk()  # Neues Fenster für das Spiel
    game_window.title("Minesweeper")
    width, height = map(int, geometry.split('x'))
    center_window(game_window, width, height)  # Zentriert das Fenster auf dem Bildschirm
    Minesweeper(game_window, rows, cols, mines)  # Initialisiert das Spiel
    try:
        menu_window.destroy()  # Schließt das Menüfenster, sobald das Spiel startet
    finally:
        game_window.mainloop()  # Startet die Hauptschleife des Spiels


# Zeigt die Bestenliste an
def show_leaderboard():
    leaderboard_window = tk.Toplevel(menu_window)  # Neues Fenster für die Bestenliste
    leaderboard_window.title("Top-Listen")
    center_window(leaderboard_window, 250, 300)
    leaderboard_window.configure(bg="#1c1c1c")  # Hintergrundfarbe des Fensters
    leaderboards = Minesweeper.load_leaderboard()  # Lädt die Bestenliste aus der Datei
    for difficulty, times in leaderboards.items():
        # Zeigt die Bestzeiten für jede Schwierigkeitsstufe an
        create_label(leaderboard_window,
                     text=f"{difficulty} --> Bestzeiten: {', '.join([f'{time:.2f}s' for time in times])}",
                     font=("Helvetica", 16, "bold"),
                     pack_opts={'side': 'top'})


# Erstellt ein Fenster für benutzerdefinierte Spieleinstellungen
def custom_game():
    custom_window = tk.Toplevel(menu_window)
    custom_window.title("Benutzerdefinierte Einstellungen")
    center_window(custom_window, 150, 200)
    custom_window.configure(bg="#1c1c1c")

    # Eingabefelder für Reihen, Spalten und Minen
    create_label(custom_window, "Reihen (max 30):", font=("Helvetica", 11)).pack()
    rows_entry = tk.Entry(custom_window)
    rows_entry.pack()

    create_label(custom_window, "Spalten (max 30):", font=("Helvetica", 11)).pack()
    cols_entry = tk.Entry(custom_window)
    cols_entry.pack()

    create_label(custom_window, "Minen (max 800):", font=("Helvetica", 11)).pack()
    mines_entry = tk.Entry(custom_window)
    mines_entry.pack()

    # Bestätigungsfunktion für benutzerdefinierte Spieleinstellungen
    def submit_custom():
        try:
            # Hole die Werte aus den Eingabefeldern und prüfe sie
            rows = int(rows_entry.get())
            cols = int(cols_entry.get())
            mines = int(mines_entry.get())

            # Überprüfen, ob einer der Werte außerhalb des erlaubten Bereichs liegt
            if (rows < 1 or rows > 30) or (cols < 1 or cols > 30) or (mines > 800 or mines < 2):
                raise ValueError(
                    "Fehler, bitte überprüfen Sie Ihre Eingabe!")

            # Begrenze die Werte, falls sie innerhalb der erlaubten Grenzen liegen
            rows = min(30, rows)
            cols = min(30, cols)
            mines = min(800, mines)

            geo_row = int(rows * 31.25)  # Berechnet die Fenstergröße basierend auf der Anzahl der Reihen
            geo_col = int(cols * 30)  # Berechnet die Fenstergröße basierend auf der Anzahl der Spalten
            geometry = f"{geo_row}x{geo_col}"

        except ValueError as e:
            # Fehlermeldung, wenn ungültige Werte eingegeben wurden oder die Grenze überschritten wurde
            messagebox.showerror("Eingabefehler", str(e))
            return

        start_game(rows, cols, mines, geometry)  # Startet das Spiel mit den benutzerdefinierten Einstellungen
        try:
            custom_window.destroy()  # Schließt das Fenster für benutzerdefinierte Einstellungen
            menu_window.destroy()  # Schließt das Menüfenster
        finally:
            return

    # Button erstellen, um das Spiel zu starten
    create_button(custom_window, "Spiel starten", submit_custom).pack()


# Zentriert das Fenster auf dem Bildschirm
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - width / 2)
    center_y = int(screen_height / 2 - height / 2)
    root.geometry(f'+{center_x}+{center_y}')  # Setzt die Fensterposition


if __name__ == "__main__":
    menu_window = tk.Tk()  # Erstellt das Hauptmenüfenster
    menu_window.title("Minesweeper Menü")
    center_window(menu_window, 450, 450)
    menu_window.configure(bg="#1c1c1c")

    # Erstellung und Platzierung der Menüelemente
    create_label(menu_window, "Minesweeper", font=("Helvetica", 24, "bold"))
    create_button(menu_window, "Leicht (8x8, 10 Minen)", lambda: start_game(8, 8, 10, '290x210'))
    create_button(menu_window, "Mittel (16x16, 40 Minen)", lambda: start_game(16, 16, 40, '495x420'))
    create_button(menu_window, "Schwer (30x16, 99 Minen)", lambda: start_game(30, 16, 99, '500x780'))
    create_button(menu_window, "Benutzerdefiniert", custom_game)
    create_button(menu_window, "Bestenliste", show_leaderboard)

    menu_window.mainloop()  # Startet die Hauptschleife des Menüs
