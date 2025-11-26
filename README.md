# 🏀 Basketball Scoreboard

Tabellone segnapunti digitale per basket con interfaccia dual-screen professionale. Perfetto per palestre, tornei amatoriali o allenamenti.

## 📋 Caratteristiche

- 🖥️ **Dual Screen Support**: Tabellone su uno schermo, controller sull'altro
- ⏱️ **Cronometro Professionale**: Timer configurabile con allarme sonoro
- 🎯 **Gestione Completa**: Punteggi, periodi (quarti + overtime), nomi squadre
- ⌨️ **Controlli Rapidi**: Barra spaziatrice per START/STOP
- 🎨 **Design Chiaro**: Font LCD professionali, colori ad alto contrasto
- 🔊 **Allarme Sonoro**: Buzzer automatico allo scadere del tempo
- 🎮 **Controller Intuitivo**: Interfaccia semplice per gestire la partita

## 🛠️ Prerequisiti

- Python 3.11+
- Due monitor collegati al computer (uno per il tabellone, uno per il controller)
- Sistema operativo: Windows, macOS o Linux

## 📦 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/vincenzo97m/BasketScoreBoard.git
cd BasketScoreBoard
```

### 2. Crea ambiente virtuale

```bash
python -m venv .venv
source .venv/bin/activate  # Su Linux/Mac
.venv\Scripts\activate     # Su Windows
```

### 3. Installa dipendenze

```bash
pip install pygame screeninfo
```

### 4. Verifica la presenza dei file

Assicurati che la struttura sia:
```
BasketScoreBoard/
├── main.py
├── data/
│   └── Buzzer.wav
└── README.md
```

**Nota:** Il file `Buzzer.wav` deve essere nella cartella `data/` per il suono dell'allarme.

## ⚙️ Configurazione Monitor

### Setup Dual Screen

Prima di avviare l'applicazione, configura i monitor:

**Windows:**
1. `Impostazioni > Sistema > Schermo`
2. Seleziona il monitor che vuoi usare per il **tabellone**
3. Spunta "Imposta come schermo principale"
4. Il secondo monitor mostrerà automaticamente il **controller**

**macOS:**
1. `Preferenze di Sistema > Monitor`
2. Trascina la barra bianca sul monitor che vuoi come principale
3. Il monitor principale mostrerà il **tabellone**

**Linux:**
1. Usa le impostazioni del display manager
2. Imposta come primario il monitor per il **tabellone**

### Configurazione Consigliata

- **Monitor Principale (Tabellone)**: TV/Proiettore visibile da tutti
- **Monitor Secondario (Controller)**: Laptop/Monitor vicino al tavolo segnapunti

## 🚀 Utilizzo

### Avvio Applicazione

```bash
python main.py
```

### Primo Avvio

Al primo avvio appariranno dei messaggi:

1. **Controllo Monitor**: Verifica presenza secondo monitor
2. **Impostazioni Display**: Conferma che il monitor principale sia configurato
3. **Nomi Squadre**: Inserisci i nomi delle squadre (o usa HOME/GUEST di default)

### Interfaccia Controller

Il **controller** (schermo secondario) mostra:

```
┌─────────────────────────────────────┐
│  +HOME    │  + Period  │  +GUEST   │
│     0     │    1QT     │     0     │
│  -HOME    │  - Period  │  -GUEST   │
├─────────────────────────────────────┤
│ Set Timer │   START    │Reset Timer│
│           │   10:00    │           │
│Nome HOME  │            │Nome GUEST │
└─────────────────────────────────────┘
```

### Interfaccia Tabellone

Il **tabellone** (schermo principale) mostra:

```
┌─────────────────────────────────────┐
│            10:00                    │
├─────────────────────────────────────┤
│  HOME     │   1QT    │    GUEST    │
│    0      │          │      0      │
└─────────────────────────────────────┘
```

## 🎮 Controlli

### Punteggi

| Pulsante | Azione |
|----------|--------|
| **+HOME** | Aggiunge 1 punto alla squadra HOME |
| **-HOME** | Toglie 1 punto alla squadra HOME |
| **+GUEST** | Aggiunge 1 punto alla squadra GUEST |
| **-GUEST** | Toglie 1 punto alla squadra GUEST |

### Periodi

| Pulsante | Azione |
|----------|--------|
| **+ Period** | Passa al periodo successivo |
| **- Period** | Torna al periodo precedente |

**Periodi disponibili:** 1QT → 2QT → 3QT → 4QT → 1OT → 2OT → 3OT → ... → 9OT

### Cronometro

| Pulsante | Azione |
|----------|--------|
| **Set Timer** | Imposta tempo personalizzato (minuti e secondi) |
| **START** | Avvia il cronometro (diventa rosso "STOP") |
| **STOP** | Ferma il cronometro (diventa verde "START") |
| **Reset Timer** | Riporta il timer a 10:00 |
| **Barra Spaziatrice** | START/STOP rapido dalla tastiera |

### Nomi Squadre

| Pulsante | Azione |
|----------|--------|
| **Nome HOME** | Cambia il nome della squadra HOME |
| **Nome GUEST** | Cambia il nome della squadra GUEST |

## ⏱️ Gestione Tempo

### Impostazione Timer

1. Clicca **"Set Timer"**
2. Inserisci i **minuti** (0-10)
3. Inserisci i **secondi** (0-59)
4. Il timer si aggiorna automaticamente

**Esempio:** Per impostare 8 minuti e 30 secondi:
- Minuti: `8`
- Secondi: `30`

### Comportamento Timer

- ⏯️ **START**: Il timer inizia a decrementare ogni secondo
- ⏸️ **STOP**: Il timer si ferma mantenendo il tempo attuale
- 🔄 **Reset**: Riporta il timer a 10:00 (tempo iniziale di default)
- 🔊 **Allarme**: Quando il timer arriva a 0:00, suona automaticamente il buzzer

### Scorciatoia Tastiera

**Barra Spaziatrice** = START/STOP istantaneo
- Utile per fermare rapidamente il tempo durante i falli
- Non serve cliccare il pulsante con il mouse

## 🎨 Personalizzazione

### Font

L'applicazione usa font LCD professionali:
- **Punteggi**: `2 5x9 Scoreboard` (125pt)
- **Tempo**: `2 5x9 Scoreboard` (120pt)
- **Periodo**: `LCD Solid` (80pt)

**Nota:** Se i font non sono installati, il sistema userà font di fallback.

### Colori

- **Sfondo**: Nero (massima leggibilità)
- **Punteggi**: Verde (visibilità ottimale)
- **Tempo/Periodo**: Rosso (attenzione immediata)
- **Nomi Squadre**: Bianco

### Modificare il Tempo Iniziale

Nel file `main.py`, modifica la costante:

```python
INITIAL_TIME_MS = 600  # 10 minuti in secondi
```

**Esempi:**
- 8 minuti: `INITIAL_TIME_MS = 480`
- 12 minuti: `INITIAL_TIME_MS = 720`
- 5 minuti: `INITIAL_TIME_MS = 300`

### Cambiare il Suono del Buzzer

Sostituisci il file `data/Buzzer.wav` con il tuo file audio preferito (formato WAV).

## 🔧 Risoluzione Problemi

### Il secondo monitor non viene rilevato

**Soluzione:**
1. Verifica che il monitor sia collegato e acceso
2. Controlla nelle impostazioni di sistema che sia rilevato
3. Riavvia l'applicazione dopo aver collegato il monitor

**Modalità un solo monitor:**
L'app chiederà se vuoi continuare ugualmente. Entrambe le finestre appariranno sullo stesso schermo (meno ideale ma funzionale).

### I font non vengono visualizzati correttamente

**Soluzione:**
- I font LCD potrebbero non essere installati nel sistema
- L'applicazione userà font di fallback (Arial)
- Per installare i font: copia i file `.ttf` nella cartella Font di sistema

### Il suono dell'allarme non funziona

**Soluzione:**
1. Verifica che `data/Buzzer.wav` esista
2. Controlla che il volume del sistema sia attivo
3. Verifica che pygame sia installato: `pip install pygame`

### Le finestre non sono a schermo intero

**Soluzione:**
- Premi `F11` sul tabellone per attivare fullscreen
- Oppure modifica il codice per forzare fullscreen su entrambi i monitor

### I pulsanti non rispondono

**Soluzione:**
- Assicurati che la finestra controller abbia il focus
- Clicca sulla finestra controller prima di usare i pulsanti o la barra spaziatrice

## 📊 Scenari d'Uso

### Partita Standard

1. Avvia l'app e inserisci nomi squadre
2. Il timer parte già a 10:00 (primo quarto)
3. Premi **START** o **Barra Spaziatrice** all'inizio del quarto
4. Aggiorna punteggi durante il gioco
5. Al termine del quarto: **STOP** + **+ Period**
6. Usa **Reset Timer** per riportare a 10:00
7. Ripeti per tutti i 4 quarti

### Overtime

1. Dopo il 4° quarto, premi **+ Period** per passare a **1OT**
2. Imposta timer overtime: **Set Timer** → 5 minuti
3. Continua il gioco normalmente
4. Supporto fino a 9 overtime

### Allenamento/Scrimmage

1. Usa **Set Timer** per impostare durata personalizzata
2. Non cambiare periodo se non necessario
3. Usa **Reset Timer** per sessioni multiple

## 📁 Struttura del Progetto

```
BasketScoreBoard/
├── main.py                    # Applicazione principale
├── data/
│   └── Buzzer.wav            # Suono allarme
├── .idea/                    # Configurazione IDE (PyCharm)
│   ├── .gitignore
│   ├── BasketScoreBoard.iml
│   ├── inspectionProfiles/
│   ├── misc.xml
│   ├── modules.xml
│   └── vcs.xml
├── .venv/                    # Ambiente virtuale (non nel repo)
└── README.md                 # Questo file
```

## 🔒 Note sulla Privacy

Questo è un progetto ad **uso personale/locale**. Non raccoglie né trasmette dati.

## 📜 Licenza

Progetto ad uso privato e personale.

## 👤 Autore

**vincenzo97m**

## 💡 Suggerimenti

- 🖥️ Usa un **TV/Proiettore grande** per il tabellone
- ⌨️ Tieni una **tastiera wireless** vicino al tavolo segnapunti per controllo rapido
- 🔊 Collega **speaker esterni** per un buzzer più potente
- 📱 In alternativa, puoi usare un **tablet** come controller con software di desktop remoto
- 🎥 Per streaming: usa software come OBS per catturare solo la finestra del tabellone

## 🚀 Sviluppi Futuri (Opzionale)

- [ ] Statistiche giocatori (falli, assist, rimbalzi)
- [ ] Salvataggio partite
- [ ] Modalità torneo con bracket
- [ ] Controllo remoto via web/mobile
- [ ] Skin/temi personalizzabili
- [ ] Export risultati in PDF

---

**⚡ Pro Tip:** Configura un hotkey di sistema per rendere fullscreen la finestra del tabellone con un singolo tasto!

**🏀 Buona Partita!**
