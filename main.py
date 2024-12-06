import tkinter as tk
from tkinter import font, simpledialog, messagebox

# Funzioni per aggiornare il punteggio, il periodo, e il tempo
def update_score(label, increment):
    current = int(label["text"])
    new_score = max(0, current + increment)  # Non permettere punteggi negativi
    label.config(text=str(new_score))
    update_replica()  # Aggiorna la replica del tabellone

def update_period(label, increment):
    current = label["text"]
    period_values = ["1", "2", "3", "4", "1OT", "2OT", "3OT", "4OT", "5OT", "6OT", "7OT", "8OT", "9OT"]
    try:
        current_index = period_values.index(current)
        new_index = (current_index + increment) % len(period_values)
        label.config(text=period_values[new_index])
    except ValueError:
        label.config(text="1")  # Default to 1 if not found
    update_replica()  # Aggiorna la replica del tabellone

def update_time(label, minutes, seconds):
    label.config(text=f"{minutes}:{seconds:02d}")
    update_replica()  # Aggiorna la replica del tabellone

def set_time():
    # Mostra finestra per inserire minuti e secondi
    minutes = simpledialog.askinteger("Imposta Tempo", "Inserisci i minuti:")
    if minutes is None:
        return

    seconds = simpledialog.askinteger("Imposta Tempo", "Inserisci i secondi:")
    if seconds is None:
        return

    global remaining_time
    remaining_time = minutes * 60 + seconds  # Calcola il tempo totale in secondi
    update_time(time_label, minutes, seconds)
    start_stop_button.config(state="normal")  # Attiva il pulsante di avvio

def start_stop_timer():
    global running, remaining_time
    if running:
        running = False
        start_stop_button.config(text="START")
    else:
        running = True
        start_stop_button.config(text="STOP")
        start_timer()

def start_timer():
    global remaining_time
    if running and remaining_time > 0:
        remaining_time -= 1
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        update_time(time_label, minutes, seconds)
        tabellone.after(1000, start_timer)  # Decrementa ogni secondo

def change_team_name(team):
    new_name = simpledialog.askstring("Nome Squadra", f"Inserisci il nome della squadra {team}:")
    if team == "locali" and new_name:
        locali_label.config(text=new_name.upper())
    elif team == "ospiti" and new_name:
        ospiti_label.config(text=new_name.upper())

def on_close_controller():
    result = messagebox.askquestion("Conferma Chiusura", "Sei sicuro di voler chiudere Tabellone Segnapunti?")
    if result == 'yes':
        tabellone.quit()
        controller.quit()

def update_replica():
    # Aggiorna la replica del tabellone ogni volta che avviene una modifica
    locali_score_replica.config(text=locali_score["text"])
    ospiti_score_replica.config(text=ospiti_score["text"])
    period_value_replica.config(text=period_value["text"])
    time_label_replica.config(text=time_label["text"])

# Flag per controllare il timer
running = False
remaining_time = 600  # Tempo iniziale (10:00 minuti)

# Creazione della finestra per il tabellone
tabellone = tk.Tk()
tabellone.title("Tabellone Segnapunti Basket")
tabellone.attributes("-fullscreen", False)  # Imposta a schermo intero
tabellone.configure(bg="black")  # Cambia colore di sfondo a nero

# Configurazione dei font con dimensioni adattate alla risoluzione
score_font = font.Font(family="Arial", size=180, weight="bold")  # Ridotto per 1920x1080
period_font = font.Font(family="Arial", size=100, weight="bold")  # Ridotto per 1920x1080
time_font = font.Font(family="Arial", size=140, weight="bold")  # Ridotto per 1920x1080
small_font = font.Font(family="Arial", size=40, weight="bold")  # Font per testo piccolo

# Punteggio Locali
locali_label = tk.Label(tabellone, text="HOME", bg="black", fg="white", font=small_font)
locali_label.grid(row=0, column=0, padx=20, pady=10)

locali_score = tk.Label(tabellone, text="0", bg="black", fg="green", font=score_font)
locali_score.grid(row=1, column=0, padx=20)

# Punteggio Ospiti
ospiti_label = tk.Label(tabellone, text="VISITOR", bg="black", fg="white", font=small_font)
ospiti_label.grid(row=0, column=2, padx=40, pady=10)

ospiti_score = tk.Label(tabellone, text="0", bg="black", fg="green", font=score_font)
ospiti_score.grid(row=1, column=2, padx=40)

# Periodo
period_label = tk.Label(tabellone, text="PERIOD", bg="black", fg="white", font=small_font)
period_label.grid(row=0, column=1, padx=20)

period_value = tk.Label(tabellone, text="1", bg="black", fg="red", font=period_font)
period_value.grid(row=1, column=1)

# Tempo rimanente
time_label = tk.Label(tabellone, text="10:00", bg="black", fg="red", font=time_font)
time_label.grid(row=2, column=1, pady=20)

# Finestra del controller
controller = tk.Tk()
controller.title("Controller - Segnapunti")
controller.geometry("800x600")  # Imposta una finestra di dimensioni moderate
controller.configure(bg="black")

controller.protocol("WM_DELETE_WINDOW", on_close_controller)  # Chiusura finestra con conferma

# Replica del tabellone nel controller
replica_tabellone = tk.Frame(controller, bg="black")
replica_tabellone.grid(row=0, column=1, padx=20, pady=20)

locali_score_replica = tk.Label(replica_tabellone, text="0", bg="black", fg="green", font=score_font)
locali_score_replica.grid(row=1, column=0, padx=20)

ospiti_score_replica = tk.Label(replica_tabellone, text="0", bg="black", fg="green", font=score_font)
ospiti_score_replica.grid(row=1, column=2, padx=20)

period_value_replica = tk.Label(replica_tabellone, text="1", bg="black", fg="red", font=period_font)
period_value_replica.grid(row=1, column=1)

time_label_replica = tk.Label(replica_tabellone, text="10:00", bg="black", fg="red", font=time_font)
time_label_replica.grid(row=2, column=1, pady=20)

# Pulsanti nel controller
button_frame = tk.Frame(controller, bg="black")
button_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

button_frame.grid_rowconfigure(0, weight=1)
button_frame.grid_rowconfigure(1, weight=1)
button_frame.grid_rowconfigure(2, weight=1)
button_frame.grid_rowconfigure(3, weight=1)
button_frame.grid_rowconfigure(4, weight=1)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

# Pulsanti per modificare il punteggio e periodo
add_locali_button = tk.Button(button_frame, text="+HOME", font=("Arial", 50), bg="white", command=lambda: update_score(locali_score, 1))
add_locali_button.grid(row=0, column=0, padx=10, pady=10)

sub_locali_button = tk.Button(button_frame, text="-HOME", font=("Arial", 50), bg="white", command=lambda: update_score(locali_score, -1))
sub_locali_button.grid(row=1, column=0, padx=10, pady=10)

change_locali_name_button = tk.Button(button_frame, text="Cambia Nome HOME", font=small_font, command=lambda: change_team_name("locali"))
change_locali_name_button.grid(row=3, column=0, padx=10, pady=10)

# Pulsanti Ospiti
add_ospiti_button = tk.Button(button_frame, text="+VISITOR", font=("Arial", 50), bg="white", command=lambda: update_score(ospiti_score, 1))
add_ospiti_button.grid(row=0, column=2, padx=10, pady=10)

sub_ospiti_button = tk.Button(button_frame, text="-VISITOR", font=("Arial", 50), bg="white", command=lambda: update_score(ospiti_score, -1))
sub_ospiti_button.grid(row=1, column=2, padx=10, pady=10)

change_ospiti_name_button = tk.Button(button_frame, text="Cambia Nome VISITOR", font=small_font, command=lambda: change_team_name("ospiti"))
change_ospiti_name_button.grid(row=3, column=2, padx=10, pady=10)

# Pulsanti al centro
set_time_button = tk.Button(button_frame, text="Imposta Tempo", font=small_font, bg="white", command=set_time)
set_time_button.grid(row=0, column=1, padx=10, pady=10)

change_period_button = tk.Button(button_frame, text="+ Period", font=small_font, bg="white", command=lambda: update_period(period_value, 1))
change_period_button.grid(row=1, column=1, padx=10, pady=10)

decrease_period_button = tk.Button(button_frame, text="- Period", font=small_font, bg="white", command=lambda: update_period(period_value, -1))
decrease_period_button.grid(row=2, column=1, padx=10, pady=10)

start_stop_button = tk.Button(button_frame, text="START", font=("Arial", 60), bg="green", command=start_stop_timer)
start_stop_button.grid(row=3, column=1, padx=10, pady=10)

controller.mainloop()
