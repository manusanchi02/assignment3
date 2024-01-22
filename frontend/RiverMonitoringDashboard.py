import serial.tools.list_ports
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import requests

# Imposto url server
url = 'http://localhost:8080'

# Dati
x = [] # Andamento orario
y = [] # Valori altezza acqua

# Attiva la modalità interattiva di matplotlib
plt.ion()

# Crea un'istanza del grafico
fig, ax = plt.subplots()
line, = ax.plt([], [])  # Creazione di una linea vuota

# Imposta i limiti degli assi
ax.set_xlim(0, 20)
ax.set_ylim(0, 10)

# Titoli ed etichette
ax.set_title('Grafico Altezza Acqua')
ax.set_xlabel('Tempo')
ax.set_ylabel('Altezza Acqua')

layout = [
    [sg.Text('Finestra con Grafico')],
    [sg.Text('Status:') ,sg.Text("Reading...",key='-ERROR-')]
    [sg.Canvas(key='-CANVAS-')],
    [sg.Text('Valve:'), sg.Text('Closed', key='-VALVE-')],
    [sg.Button('Apri',key='bottoneA-C')],
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
    
    if event == 'bottoneA-C':
        if(window['-VALVE-'].get()=="Closed"):
            window['-VALVE-'].update("Open")
            requests.post(url, data="Valve:Open")
            window['bottoneA-C'].update(text='Chiudi')
        else:
            window['-VALVE-'].update("Closed")
            requests.post(url, data="Valve:Closed")
            window['bottoneA-C'].update(text='Apri')

    # Aggiorna ogni 0.1 secondi
    time.sleep(0.1)

    # Richiesta HTTP
    response = requests.get(url)

    # Verifica dello stato della risposta
    if response.status_code == 200:
        # La richiesta è andata a buon fine
        elementi_divisi = response.split(';')
        for elemento in elementi_divisi:
            dato = elemento.split(":")
            if(dato[0]== "State"):
                window['-ERROR-'].update(dato[1])
                print("Normale")
            elif(dato[0]=="Water_level"):
                y.append(dato[1])
                x.append(time.time())
                if(x.length > 20):
                    x.pop(0)
                    y.pop(0)
                aggiorna_grafico(x, y)
            elif(dato[0]=="Valve"):
                window['-VALVE-'].update(dato[1])
                if(dato[1]=="Open"):
                    window['bottoneA-C'].update(text='Chiudi')
                else:
                    window['bottoneA-C'].update(text='Apri')
                print("Emergenza!")
            else:
                print("Errore nella risposta del server")
        
    else:
        # Gestione degli errori
        print(f"Errore nella richiesta HTTP. Codice di stato: {response.status_code}")