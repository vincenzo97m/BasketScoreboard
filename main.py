import tkinter as tk
from tkinter import font, simpledialog, messagebox
import pygame
from screeninfo import get_monitors

# Inizializza pygame per gestire il suono
pygame.mixer.init()

# Funzione per riprodurre il suono
def play_alarm_sound():
    pygame.mixer.music.load("Buzzer.wav")  # Carica il file audio (modifica il percorso se necessario)
    pygame.mixer.music.play()  # Riproduce il suono

# Funzione per spostare la finestra nel monitor secondario
def set_fullscreen_on_secondary_screen():
    monitors = get_monitors()  # Ottieni tutte le informazioni sugli schermi connessi
    if len(monitors) > 1:
        # Se ci sono più monitor, seleziona il secondo (secondario)
        secondary_monitor = monitors[1]

        # Imposta la finestra per il monitor secondario
        tabellone.lift()
        tabellone.geometry(
            f"{secondary_monitor.width}x{secondary_monitor.height}+{secondary_monitor.x}+{secondary_monitor.y}")
        tabellone.attributes('-fullscreen', True)  # Rendi la finestra fullscreen
    else:
        print("Non ci sono schermi secondari connessi.")

# Funzioni per gestire il tabellone
def update_score(label, increment, display_label=None):
    """Aggiorna il punteggio di una squadra e, se fornito, aggiorna anche l'etichetta nel controller."""
    current = int(label["text"])
    new_score = max(0, current + increment)
    label.config(text=str(new_score))
    if display_label:
        display_label.config(text=str(new_score))  # Aggiorna l'etichetta nel controller

def update_period(label, increment, period_display_label=None):
    """Aggiorna il periodo del gioco e, se fornito, aggiorna anche l'etichetta nel controller."""
    period_values = ["1QT", "2QT", "3QT", "4QT", "1OT", "2OT", "3OT", "4OT", "5OT", "6OT", "7OT", "8OT", "9OT"]
    try:
        current_index = period_values.index(label["text"])
        new_index = (current_index + increment) % len(period_values)
        label.config(text=period_values[new_index])
        if period_display_label:
            period_display_label.config(text=period_values[new_index])  # Aggiorna l'etichetta nel controller
    except ValueError:
        label.config(text="1QT")

def update_time(label, minutes, seconds, time_display_label=None):
    """Aggiorna il tempo visualizzato e, se fornito, aggiorna anche l'etichetta nel controller."""
    label.config(text=f"{minutes}:{seconds:02d}")
    if time_display_label:
        time_display_label.config(text=f"{minutes}:{seconds:02d}")  # Aggiorna l'etichetta nel controller

def set_time():
    """Imposta il tempo iniziale."""
    minutes = simpledialog.askinteger("Imposta Tempo", "Inserisci solo il numero dei minuti (da 0 a 10), se 0 scrivi 0:")
    if minutes is None or minutes > 10:
        return
    seconds = simpledialog.askinteger("Imposta Tempo", "Inserisci solo il numero dei secondi (da 0 a 59), se 0 scrivi 0:")
    if seconds is None or seconds > 60:
        return
    global remaining_time
    remaining_time = max(0, minutes * 60 + seconds)
    update_time(time_label, minutes, seconds, time_label_display)
    start_stop_button.config(state="normal")

def start_stop_timer():
    """Avvia o ferma il timer."""
    global running
    running = not running
    start_stop_button.config(text="STOP" if running else "START", bg="red" if running else "green")
    if running:
        start_timer()

def reset_timer():
    """Resetta il timer al valore iniziale."""
    global running, remaining_time
    running = False
    start_stop_button.config(text="START", bg="green")
    remaining_time = 600
    update_time(time_label, 10, 0, time_label_display)

def start_timer():
    """Decrementa il timer ogni secondo."""
    global remaining_time
    if running and remaining_time > 0:
        remaining_time -= 1
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        update_time(time_label, minutes, seconds, time_label_display)
        tabellone.after(1000, start_timer)
    elif remaining_time == 0:  # Quando il tempo arriva a zero, suona l'allarme
        play_alarm_sound()

def change_team_name(team):
    """Permette di cambiare il nome della squadra."""
    new_name = simpledialog.askstring("Nome Squadra", f"Inserisci il nome della squadra {team}:")
    if new_name:
        (locali_label if team == "locali" else ospiti_label).config(text=new_name.upper())

def on_close_controller():
    """Gestisce la chiusura della finestra del controller."""
    if messagebox.askquestion("Conferma Chiusura", "Sei sicuro di voler chiudere Tabellone Segnapunti?") == 'yes':
        tabellone.quit()
        controller.quit()

# Configurazioni iniziali
running = False
remaining_time = 600

# Creazione del TABELLONE
tabellone = tk.Tk()
tabellone.title("Tabellone Segnapunti Basket")
tabellone.configure(bg="black")
tabellone.grid_anchor("center")

set_fullscreen_on_secondary_screen()

# Configura le righe e le colonne per il layout dinamico
# tabellone.grid_rowconfigure(0, weight=1)
# tabellone.grid_columnconfigure(0, weight=1)
#
# tabellone.grid_rowconfigure(1, weight=2)
# tabellone.grid_columnconfigure(1, weight=2)
#
# tabellone.grid_rowconfigure(2, weight=2)
# tabellone.grid_columnconfigure(2, weight=1)

# Font più grandi per punteggio e tempo, FONT DISPONIBILI: Arial, Score Board, LCD Solid, 2 5x9 Scoreboard
score_font = font.Font(family="2 5x9 Scoreboard", size=125, weight="bold")
period_font = font.Font(family="LCD Solid", size=80, weight="bold")
time_font = font.Font(family="2 5x9 Scoreboard", size=120, weight="bold")
small_font = font.Font(family="LCD Solid", size=70, weight="bold")

# Etichette per il punteggio
locali_label = tk.Label(tabellone, text="HOME", bg="black", fg="white", font=small_font)
locali_label.grid(row=1, column=0, pady=5)
locali_score = tk.Label(tabellone, text="120", bg="black", fg="green", font=score_font)
locali_score.grid(row=2, column=0)

ospiti_label = tk.Label(tabellone, text="VISITOR", bg="black", fg="white", font=small_font)
ospiti_label.grid(row=1, column=2, pady=5)
ospiti_score = tk.Label(tabellone, text="120", bg="black", fg="green", font=score_font)
ospiti_score.grid(row=2, column=2)

# Etichetta per il periodo
# period_label = tk.Label(tabellone, text="PERIOD", bg="black", fg="white", font=period_font)
# period_label.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

# Valore del periodo
period_value = tk.Label(tabellone, text="1QT", bg="black", fg="red", font=period_font)
period_value.grid(row=1, column=1, padx = 20)

# Etichetta per il timer
time_label = tk.Label(tabellone, text="10:00", bg="black", fg="red", font=time_font)
time_label.grid(row=0, columnspan=3, stick="nsew")

# Creazione del CONTROLLER
controller = tk.Tk()
controller.title("Controller - Segnapunti")
controller.configure(bg="black")
controller.grid_anchor("center")
controller.protocol("WM_DELETE_WINDOW", on_close_controller)

button_frame = tk.Frame(controller, bg="blue")
button_frame.grid(row=0, column=0, padx=20, pady=20)

# Etichette per visualizzare i punteggi nel controller
locali_score_display = tk.Label(controller, text="0", bg="black", fg="green", font=("Arial", 70))
locali_score_display.grid(row=1, column=0, padx=40)
ospiti_score_display = tk.Label(controller, text="0", bg="black", fg="green", font=("Arial", 70))
ospiti_score_display.grid(row=1, column=2, padx=40)

# Etichetta per visualizzare il periodo nel controller
period_value_display = tk.Label(controller, text="1QT", bg="black", fg="red", font=("Arial", 40))
period_value_display.grid(row=1, column=1)

# Etichetta per visualizzare il tempo nel controller
time_label_display = tk.Label(controller, text="10:00", bg="black", fg="red", font=("Arial", 70))
time_label_display.grid(row=4, column=1)

# Pulsanti HOME del controller
tk.Button(controller, text="+HOME", font=("Arial", 50), bg="white", command=lambda: update_score(locali_score, 1, locali_score_display)).grid(row=0, column=0)
tk.Button(controller, text="-HOME", font=("Arial", 50), bg="white", command=lambda: update_score(locali_score, -1, locali_score_display)).grid(row=2, column=0)

# Pulsanti VISITOR del controller
tk.Button(controller, text="+VISITOR", font=("Arial", 50), bg="white", command=lambda: update_score(ospiti_score, 1, ospiti_score_display)).grid(row=0, column=2)
tk.Button(controller, text="-VISITOR", font=("Arial", 50), bg="white", command=lambda: update_score(ospiti_score, -1, ospiti_score_display)).grid(row=2, column=2)

# Pulsanti PERIOD del controller
tk.Button(controller, text="+ Period", font=("Arial", 30), bg="white", command=lambda: update_period(period_value, 1, period_value_display)).grid(row=0, column=1)
tk.Button(controller, text="- Period", font=("Arial", 30), bg="white", command=lambda: update_period(period_value, -1, period_value_display)).grid(row=2, column=1)

#  Pulsanti TIMER del controller
tk.Button(controller, text="Imposta Tempo", font=small_font, bg="white", command=set_time).grid(row=3, column=0)
start_stop_button = tk.Button(controller, text="START", font=("Arial", 60), bg="green", command=start_stop_timer)
start_stop_button.grid(row=3, column=1)
tk.Button(controller, text="Reset Timer", font=small_font, bg="white", command=reset_timer).grid(row=3, column=2)

# Pulsanti per cambiare i nomi delle squadre
tk.Button(controller, text="Cambia Nome HOME", font=small_font, bg="white", command=lambda: change_team_name("locali")).grid(row=4, column=0, pady=10)
tk.Button(controller, text="Cambia Nome VISITOR", font=small_font, bg="white", command=lambda: change_team_name("ospiti")).grid(row=4, column=2, pady=10)

print("\n********************************************************************")
print("Prima dell'avvio in impostazioni >> sistema >> schermo \nselezionare il monitor secondario e spuntare \"Imposta come schermo principale\"")
print("********************************************************************")
print("\nHandcrafted by Vincenzo Morabito\n")
print("********************************************************************")

controller.mainloop()
