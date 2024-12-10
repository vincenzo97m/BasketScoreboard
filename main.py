import tkinter as tk
from tkinter import font, simpledialog, messagebox
import pygame
from screeninfo import get_monitors

#COSTANTI
INITIAL_TIME_MS = 600  # 10 minuti in millisecondi

# Inizializza pygame per gestire il suono
pygame.mixer.init()

# Funzione per riprodurre il suono
def play_alarm_sound():
    pygame.mixer.music.load("data/Buzzer.wav")  # Carica il file audio (modifica il percorso se necessario)
    pygame.mixer.music.play()  # Riproduce il suono

# Funzione per aprire la finestra CONTROLLER sul monitor secondario
def set_controller_on_secondary_screen():
    monitors = get_monitors()  # Ottieni tutte le informazioni sugli schermi connessi
    if len(monitors) > 1:
        # Se ci sono più monitor, seleziona il secondario
        primary_monitor = monitors[0]
        # Imposta la finestra per il monitor secondario
        controller.geometry(
            f"{primary_monitor.width}x{primary_monitor.height}+{primary_monitor.x}+{primary_monitor.y}")

# Funzione per aprire la finestra TABELLONE sul monitor secondario
def set_fullscreen_on_primary_screen():
    monitors = get_monitors()  # Ottieni tutte le informazioni sugli schermi connessi
    if len(monitors) > 1:
        secondary_monitor = monitors[1] # Se ci sono più monitor, seleziona quello principale
        # Imposta la finestra per il monitor principale
        tabellone.geometry(
            f"{secondary_monitor.width}x{secondary_monitor.height}+{secondary_monitor.x}+{secondary_monitor.y}")
        # Rendi la finestra fullscreen
        tabellone.attributes('-fullscreen', True)

# Funzioni per gestire il tabellone
def update_score(label, increment, display_label=None):
    """Aggiorna il punteggio di una squadra e, se fornito, aggiorna anche l'etichetta nel CONTROLLER."""
    current = int(label["text"])
    new_score = max(0, current + increment)
    label.config(text=str(new_score))
    display_label.config(text=str(new_score))  # Aggiorna l'etichetta nel CONTROLLER

def update_period(label, increment, period_display_label=None):
    """Aggiorna il periodo del gioco e, se fornito, aggiorna anche l'etichetta nel CONTROLLER."""
    period_values = ["1QT", "2QT", "3QT", "4QT", "1OT", "2OT", "3OT", "4OT", "5OT", "6OT", "7OT", "8OT", "9OT"]
    try:
        current_index = period_values.index(label["text"])
        new_index = (current_index + increment) % len(period_values)
        label.config(text=period_values[new_index])
        period_display_label.config(text=period_values[new_index])  # Aggiorna l'etichetta nel CONTROLLER
    except ValueError:
        label.config(text="1QT")

def update_time(label, minutes, seconds, time_display_label=None):
    """Aggiorna il tempo visualizzato (minuti:secondi o secondi:millesimi)."""
    label.config(text=f"{minutes}:{seconds:02}")
    time_display_label.config(text=f"{minutes}:{seconds:02}")

def set_time():
    """Imposta il tempo iniziale."""
    minutes = simpledialog.askinteger("Imposta Tempo", "Inserisci solo il numero dei minuti (da 0 a 10), se 0 scrivi 0:", parent=controller)
    if minutes is None or minutes > 10:
        return
    seconds = simpledialog.askinteger("Imposta Tempo", "Inserisci solo il numero dei secondi (da 0 a 59), se 0 scrivi 0:", parent=controller)
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
    remaining_time = INITIAL_TIME_MS
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

def change_team_name(team, parent):
    """Permette di cambiare il nome della squadra."""
    new_name = simpledialog.askstring(
        "Nome Squadra",
        f"Inserisci il nome della squadra {team}:",
        parent=parent  # Specifica la finestra principale come parent
    )
    if new_name:
        (locali_label if team == "HOME" else ospiti_label).config(text=new_name.upper())

def on_close_controller():
    """Gestisce la chiusura della finestra del CONTROLLER."""
    if messagebox.askquestion("Conferma Chiusura", "Sei sicuro di voler chiudere Tabellone Segnapunti?", parent=controller) == 'yes':
        tabellone.quit()
        controller.quit()

# Configurazioni iniziali
running = False
remaining_time = INITIAL_TIME_MS

# Creazione del TABELLONE
tabellone = tk.Tk()
tabellone.title("Tabellone Segnapunti Basket")
tabellone.configure(bg="black")
tabellone.grid_anchor("center")

set_fullscreen_on_primary_screen()

# Font più grandi per punteggio e tempo
score_font = font.Font(family="2 5x9 Scoreboard", size=125, weight="bold")
period_font = font.Font(family="LCD Solid", size=80, weight="bold")
time_font = font.Font(family="2 5x9 Scoreboard", size=120, weight="bold")
small_font = font.Font(family="LCD Solid", size=70, weight="bold")

# Etichette per il punteggio
locali_label = tk.Label(tabellone, text="HOME", bg="black", fg="white", font=small_font)
locali_label.grid(row=1, column=0, pady=5)
locali_score = tk.Label(tabellone, text="0", bg="black", fg="green", font=score_font)
locali_score.grid(row=2, column=0)

ospiti_label = tk.Label(tabellone, text="GUEST", bg="black", fg="white", font=small_font)
ospiti_label.grid(row=1, column=2, pady=5)
ospiti_score = tk.Label(tabellone, text="0", bg="black", fg="green", font=score_font)
ospiti_score.grid(row=2, column=2)

# Periodo e timer
period_value = tk.Label(tabellone, text="1QT", bg="black", fg="red", font=period_font)
period_value.grid(row=1, column=1, padx=20)

time_label = tk.Label(tabellone, text="10:00", bg="black", fg="red", font=time_font)
time_label.grid(row=0, columnspan=3, stick="nsew")

# Funzione per gestire la cattura della barra spaziatrice
def handle_spacebar(event):
    """Barra spaziatrice per avviare o fermare il timer."""
    start_stop_timer()
    return "break"

# Creazione del CONTROLLER
controller = tk.Tk()
controller.title("Controller - Segnapunti")
controller.configure(bg="black")
controller.grid_anchor("center")
controller.protocol("WM_DELETE_WINDOW", on_close_controller)

# Posiziona la finestra CONTROLLER sul monitor secondario
set_controller_on_secondary_screen()

# Comando per bind barra spaziatrice <---> Start/Stop Timer
controller.bind("<space>", handle_spacebar)

button_frame = tk.Frame(controller, bg="blue")

# Etichette per visualizzare i punteggi nel CONTROLLER
locali_score_display = tk.Label(controller, text="0", bg="black", fg="green", font=("Arial", 100))
locali_score_display.grid(row=1, column=0, padx=40)
ospiti_score_display = tk.Label(controller, text="0", bg="black", fg="green", font=("Arial", 100))
ospiti_score_display.grid(row=1, column=2, padx=40)

# Etichetta per visualizzare il periodo nel CONTROLLER
period_value_display = tk.Label(controller, text="1QT", bg="black", fg="red", font=("Arial", 70))
period_value_display.grid(row=1, column=1)

# Etichetta per visualizzare il tempo nel CONTROLLER
time_label_display = tk.Label(controller, text="10:00:000", bg="black", fg="red", font=("Arial", 100))
time_label_display.grid(row=4, column=1)

# Pulsanti e funzioni per il CONTROLLER
tk.Button(controller, text="+HOME", font=("Arial", 70), bg="white", command=lambda: update_score(locali_score, 1, locali_score_display)).grid(row=0, column=0)
tk.Button(controller, text="-HOME", font=("Arial", 70), bg="white", command=lambda: update_score(locali_score, -1, locali_score_display)).grid(row=2, column=0)

tk.Button(controller, text="+GUEST", font=("Arial", 70), bg="white", command=lambda: update_score(ospiti_score, 1, ospiti_score_display)).grid(row=0, column=2)
tk.Button(controller, text="-GUEST", font=("Arial", 70), bg="white", command=lambda: update_score(ospiti_score, -1, ospiti_score_display)).grid(row=2, column=2)

tk.Button(controller, text="+ Period", font=("Arial", 50), bg="white", command=lambda: update_period(period_value, 1, period_value_display)).grid(row=0, column=1)
tk.Button(controller, text="- Period", font=("Arial", 50), bg="white", command=lambda: update_period(period_value, -1, period_value_display)).grid(row=2, column=1)

tk.Button(controller, text="Set Timer", font=("Arial", 40), bg="white", command=set_time).grid(row=3, column=0)
start_stop_button = tk.Button(controller, text="START", font=("Arial", 80), bg="green", command=start_stop_timer)
start_stop_button.grid(row=3, column=1)
tk.Button(controller, text="Reset Timer", font=("Arial", 40), bg="white", command=reset_timer).grid(row=3, column=2)

tk.Button(controller, text="Nome HOME", font=("Arial", 30), bg="white", command=lambda: change_team_name("HOME", controller)).grid(row=4, column=0, pady=10)
tk.Button(controller, text="Nome GUEST", font=("Arial", 30), bg="white", command=lambda: change_team_name("GUEST", controller)).grid(row=4, column=2, pady=10)

# Mostra il messaggio informativo di un solo monitor presente.
monitorMessage = messagebox
if len(get_monitors()) == 1:
    monitorMessage = messagebox.askyesno(
        "Tabellone Segnapunti - Monitor Error",
        (
            "Non ci sono schermi secondari connessi.\n"
            "Vuoi continuare?"
        ),
        parent=controller  # Associa il messaggio alla finestra del CONTROLLER
    )
if not monitorMessage:
    exit()

# Mostra il messaggio informativo con le opzioni Sì e No
welcomeMessage = messagebox.askyesno(
    "Benvenuto",
    (
        "Benvenuto nel Segnapunti di Basket!\n\n"
        "Nel caso in cui non sia stato fatto, bisogna impostare \nlo schermo collegato come principale:\n\n"
        "1. Vai su *Impostazioni > Sistema > Schermo*.\n"
        "2. Seleziona il monitor secondario.\n"
        "3. Spunta \"Imposta come schermo principale\".\n\n"
        "Lo schermo collegato è già impostato come principale?"
    ),
    parent=controller  # Associa il messaggio alla finestra del CONTROLLER
)
# Se l'utente risponde "No", chiudi l'applicazione
if not welcomeMessage:
    exit()

infoMessage = messagebox.showinfo(
    "Nomi squadre e istruzioni",
    (
        "Per START e STOP del cronometro puoi anche usare la barra spaziatrice della tastiera.\n\n"
        "Premi OK per inserire i nomi delle squadre, se vuoi lasciare HOME e GUEST premi Cancel."
    ),
    parent=controller  # Associa il messaggio alla finestra del CONTROLLER
)
if infoMessage:
    change_team_name("HOME", controller)
    change_team_name("GUEST", controller)

controller.mainloop()
