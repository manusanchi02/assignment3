import time
import requests
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# URL del tuo server
url = "http://localhost:8080"

# Dati iniziali del grafico
x = []
y = []

# Creazione della finestra PySimpleGUI
layout = [
    [sg.Text('Stato: '), sg.Text('', key='-ERROR-')],
    [sg.Image(key='-IMAGE-')],
    [sg.Button('Esci')]
]

window = sg.Window('Grafico in tempo reale', layout, finalize=True)
plot_elem = window['-IMAGE-']

# Ciclo principale
while True:
    event, values = window.read(timeout=1000)  # Timeout di 1 secondo per evitare blocco dell'interfaccia

    if event == sg.WINDOW_CLOSED or event == 'Esci':
        break

    # Richiesta HTTP
    response = requests.get(url)
    print(response.status_code)

    # Verifica dello stato della risposta
    if response.status_code == 200:
        elementi_divisi = response.text.split(';')
        for elemento in elementi_divisi:
            dato = elemento.split(":")
            if dato[0] == "state":
                window['-ERROR-'].update(dato[1])
                print("Stato: " + dato[1])
            elif dato[0] == "water_level":
                print("Altezza acqua: " + dato[1])
                y.append(float(dato[1]))
                x.append(time.time())
                if len(x) > 20:
                    x.pop(0)
                    y.pop(0)

                # Creazione del grafico
                plt.plot(x, y, '-o', label='Altezza acqua')
                plt.legend()

                # Salvataggio dell'immagine in memoria
                buf = BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)

                # Aggiornamento dell'immagine nella finestra
                plot_elem.update(data=buf.read())

                # Pulizia della figura di Matplotlib
                plt.clf()
                buf.close()

            elif dato[0] == "valve_value":
                print("Valvola: " + dato[1])
            else:
                print("Errore nella risposta del server")
    else:
        print(f"Errore nella richiesta HTTP. Codice di stato: {response.status_code}")

# Chiusura della finestra PySimpleGUI
window.close()
