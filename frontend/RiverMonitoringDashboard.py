import serial.tools.list_ports
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import requests

# Imposto url server
url = 'http://url.controller'

# Dati
x = [] # Andamento orario
y = [] # Valori altezza acqua

# Attiva la modalità interattiva di matplotlib
plt.ion()

# Crea un'istanza del grafico
fig, ax = plt.subplots()
line, = ax.plt([], [])  # Creazione di una linea vuota

# Imposta i limiti degli assi
ax.set_xlim(0, 10)
ax.set_ylim(0, 1)

# Titoli ed etichette
ax.set_title('Grafico Altezza Acqua')
ax.set_xlabel('Tempo')
ax.set_ylabel('Altezza Acqua')

layout = [
    [sg.Text('Finestra con Grafico')],
    [sg.Text('Status:') ,sg.Text("Reading...",key='-ERROR-')]
    [sg.Canvas(key='-CANVAS-')],
    [sg.Button('Esci')]
]

window = sg.Window('Finestra con Grafico', layout, finalize=True)
canvas_elem = window['-CANVAS-']
canvas = FigureCanvasTkAgg(fig, canvas_elem.Widget)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

# Funzione per aggiornare il grafico
def aggiorna_grafico(x, y):
    line.set_xdata(x)
    line.set_ydata(y)
    fig.canvas.draw()
    fig.canvas.flush_events()

# Simulazione dei dati in tempo reale
while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Esci':
        break

    # Aggiorna ogni 0.1 secondi
    time.sleep(0.1)

    # Richiesta HTTP
    response = requests.get(url)

    # Verifica dello stato della risposta
    if response.status_code == 200:
        # La richiesta è andata a buon fine
        print(response.text)  # Contenuto della risposta
        if(response.text > 0 && response.text < 0.5):
            window['-ERROR-'].update(response.text)
            print("Normale")
        else if(response.text > 0.5):
            window['-ERROR-'].update(response.text)
            print("Allarme!")
        else if(response.text > 0.8):
            window['-ERROR-'].update(response.text)
            print("Emergenza!")
        else if(response.text > 1):
            window['-ERROR-'].update(response.text)
            print("Emergenza! Chiamare il 118!")
        else:
            y.append(response.text)
            x.append(time.time())
        
    else:
        # Gestione degli errori
        print(f"Errore nella richiesta HTTP. Codice di stato: {response.status_code}")
    
    # Aggiorna il grafico
    aggiorna_grafico(x, y)