import serial.tools.list_ports
import PySimpleGUI as sg
import matplotlib.pyplot as plot
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
line, = ax.plot([], [])  # Creazione di una linea vuota

# Imposta i limiti degli assi
ax.set_xlim(0, 10)
ax.set_ylim(0, 1)

# Titoli ed etichette
ax.set_title('Grafico Altezza Acqua')
ax.set_xlabel('Tempo')
ax.set_ylabel('Altezza Acqua')

# Funzione per aggiornare il grafico
def aggiorna_grafico(x, y):
    line.set_xdata(x)
    line.set_ydata(y)
    fig.canvas.draw()
    fig.canvas.flush_events()

# Simulazione dei dati in tempo reale
while True:
    # Aggiorna ogni 0.1 secondi
    time.sleep(0.1)

    # Richiesta HTTP
    response = requests.get(url)

    # Verifica dello stato della risposta
    if response.status_code == 200:
        # La richiesta è andata a buon fine
        print(response.text)  # Contenuto della risposta
        y.append(response.text)
        x.append(time.time())
        if(response.text > 0 && response.text < 0.5):
            print("Normale")
        if(response.text > 0.5):
            print("Allarme!")
        if(response.text > 0.8):
            print("Emergenza!")
        if(response.text > 1):
            print("Emergenza! Chiamare il 118!")
    else:
        # Gestione degli errori
        print(f"Errore nella richiesta HTTP. Codice di stato: {response.status_code}")
    
    # Aggiorna il grafico
    aggiorna_grafico(x, y)
