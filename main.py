import tkinter as tk
from tkinter import font, simpledialog, messagebox

# Funzioni per gestire il tabellone
def update_score(label, increment):
    current = int(label["text"])
    new_score = max(0, current + increment)
    label.config(text=str(new_score))

def update_period(label, increment):
    period_values = ["1", "2", "3", "4", "1OT", "2OT", "3OT", "4OT", "5OT", "6OT", "7OT", "8OT", "9OT"]
    try:
        current_index = period_values.index(label["text"])
        new_index = (current_index + increment) % len(period_values)
        label.config(text=period_values[new_index])
    except ValueError:
        label.config(text="1")

def update_time(label, minutes, seconds):
    label.config(text=f"{minutes}:{seconds:02d}")

def set_time():
    minutes = simpledialog.askinteger("Imposta Tempo", "Inserisci i minuti:")
    if minutes is None:
        return
    seconds = simpledialog.askinteger("Imposta Tempo", "Inserisci i secondi:")
    if seconds is None:
        return
    global remaining_time
    remaining_time = max(0, minutes * 60 + seconds)
    update_time(time_label, minutes, seconds)
    start_stop_button.config(state="normal")

def start_stop_timer():
    global running
    running = not running
    start_stop_button.config(text="STOP" if running else "START", bg="red" if running else "green")
    if running:
        start_timer()

def reset_timer():
    global running, remaining_time
    running = False
    start_stop_button.config(text="START", bg="green")
    remaining_time = 600
    update_time(time_label, 10, 0)

def start_timer():
    global remaining_time
    if running and remaining_time > 0:
        remaining_time -= 1
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        update_time(time_label, minutes, seconds)
        tabellone.after(1000, start_timer)

def change_team_name(team):
    new_name = simpledialog.askstring("Nome Squadra", f"Inserisci il nome della squadra {team}:")
    if new_name:
        (locali_label if team == "locali" else ospiti_label).config(text=new_name.upper())

def on_close_controller():
    if messagebox.askquestion("Conferma Chiusura", "Sei sicuro di voler chiudere Tabellone Segnapunti?") == 'yes':
        tabellone.quit()
        controller.quit()

# Configurazioni iniziali
running = False
remaining_time = 600

# Creazione del tabellone
tabellone = tk.Tk()
tabellone.title("Tabellone Segnapunti Basket")
tabellone.configure(bg="white")

score_font = font.Font(family="Arial", size=300, weight="bold")
period_font = font.Font(family="Arial", size=100, weight="bold")
time_font = font.Font(family="Arial", size=140, weight="bold")
small_font = font.Font(family="Arial", size=40, weight="bold")

locali_label = tk.Label(tabellone, text="HOME", bg="black", fg="white", font=small_font)
locali_label.grid(row=0, column=0, padx=20, pady=10)
locali_score = tk.Label(tabellone, text="0", bg="black", fg="green", font=score_font)
locali_score.grid(row=1, column=0, padx=20)

ospiti_label = tk.Label(tabellone, text="VISITOR", bg="black", fg="white", font=small_font)
ospiti_label.grid(row=0, column=2, padx=40, pady=10)
ospiti_score = tk.Label(tabellone, text="0", bg="black", fg="green", font=score_font)
ospiti_score.grid(row=1, column=2, padx=40)

period_label = tk.Label(tabellone, text="PERIOD", bg="black", fg="white", font=small_font)
period_label.grid(row=0, column=1, padx=20)
period_value = tk.Label(tabellone, text="1", bg="black", fg="red", font=period_font)
period_value.grid(row=1, column=1)

time_label = tk.Label(tabellone, text="10:00", bg="black", fg="red", font=time_font)
time_label.grid(row=2, column=1, pady=20)

# Creazione del controller
controller = tk.Tk()
controller.title("Controller - Segnapunti")
controller.configure(bg="black")
controller.protocol("WM_DELETE_WINDOW", on_close_controller)

button_frame = tk.Frame(controller, bg="black")
button_frame.grid(row=0, column=0, padx=20, pady=20)

# Pulsanti HOME con punteggio in mezzo
tk.Button(button_frame, text="+HOME", font=("Arial", 50), bg="white", command=lambda: update_score(locali_score, 1)).grid(row=0, column=0)
tk.Label(button_frame, text="0", bg="black", fg="green", font=("Arial", 50), textvariable=locali_score["text"]).grid(row=1, column=0)
tk.Button(button_frame, text="-HOME", font=("Arial", 50), bg="white", command=lambda: update_score(locali_score, -1)).grid(row=2, column=0)

# Pulsanti VISITOR con punteggio in mezzo
tk.Button(button_frame, text="+VISITOR", font=("Arial", 50), bg="white", command=lambda: update_score(ospiti_score, 1)).grid(row=0, column=2)
tk.Label(button_frame, text="0", bg="black", fg="green", font=("Arial", 50), textvariable=ospiti_score["text"]).grid(row=1, column=2)
tk.Button(button_frame, text="-VISITOR", font=("Arial", 50), bg="white", command=lambda: update_score(ospiti_score, -1)).grid(row=2, column=2)

# Pulsanti periodo con valore in mezzo
tk.Button(button_frame, text="+ Period", font=small_font, bg="white", command=lambda: update_period(period_value, 1)).grid(row=0, column=1)
tk.Label(button_frame, text="1", bg="black", fg="red", font=("Arial", 50), textvariable=period_value["text"]).grid(row=1, column=1)
tk.Button(button_frame, text="- Period", font=small_font, bg="white", command=lambda: update_period(period_value, -1)).grid(row=2, column=1)

# Timer accanto a START/STOP
tk.Button(button_frame, text="Imposta Tempo", font=small_font, bg="white", command=set_time).grid(row=3, column=0)
tk.Label(button_frame, text="10:00", bg="black", fg="red", font=("Arial", 50), textvariable=time_label["text"]).grid(row=5, column=1)
start_stop_button = tk.Button(button_frame, text="START", font=("Arial", 60), bg="green", command=start_stop_timer)
start_stop_button.grid(row=3, column=1)
tk.Button(button_frame, text="Reset Timer", font=small_font, bg="white", command=reset_timer).grid(row=3, column=2)

# Pulsanti per cambiare i nomi delle squadre
tk.Button(button_frame, text="Cambia Nome HOME", font=small_font, bg="white", command=lambda: change_team_name("locali")).grid(row=4, column=0, pady=10)
tk.Button(button_frame, text="Cambia Nome VISITOR", font=small_font, bg="white", command=lambda: change_team_name("ospiti")).grid(row=4, column=2, pady=10)

controller.mainloop()
