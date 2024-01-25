import tkinter as tk
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

# URL del tuo server
url = "http://localhost:8080"

# Dati iniziali del grafico
x = []
y = []
counter = 0

def update_plot(xValue, yValue):
    global x, y
    print(xValue)
    print(float(yValue))
    x.append(xValue)
    y.append(float(yValue))
    print(x)
    print(y)
    ax.clear()
    ax.plot(x, y)
    canvas.draw()

# Creazione della finestra principale
root = tk.Tk()
root.title("Finestra con Grafico e Slider")

headerFrame = Frame(root)
stateLabel = Label(headerFrame, text="Stato: ")
errorLabel = Label(headerFrame, text="Errore: ")
headerFrame.pack()
stateLabel.pack(side=LEFT)
errorLabel.pack(side=LEFT)

mainFrame = Frame(root)
mainFrame.pack()
# Creazione del grafico vuoto
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=mainFrame)
canvas_widget = canvas.get_tk_widget()

# Creazione dello slider
slider = ttk.Scale(mainFrame, from_=1, to=10, orient="horizontal")
slider.pack(side=BOTTOM, fill=tk.X)

# Posizionamento del grafico nella finestra
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Aggiorna il grafico con il valore iniziale dello slider
#update_plot(1)

def exit():
    sys.exit()

exitButton = Button(root,
                   text = "esci",
                   command = exit)
exitButton.pack(side=BOTTOM)


def myMainLoop():
    global counter
    # Ciclo principale
    # Richiesta HTTP
    response = requests.get(url)
    print(response.text)

    # Verifica dello stato della risposta
    if response.status_code == 200:
        elementi_divisi = response.text.split(';')
        for elemento in elementi_divisi:
            dato = elemento.split(":")
            if dato[0] == "state":
                errorLabel.config(text=f"Errore: {dato[1]}")
                print("Stato: " + dato[1])
            elif dato[0] == "water_level":
                print("Altezza acqua: " + dato[1])
                update_plot(counter, dato[1])
                #y.append(float(dato[1]))
                #x.append(counter)
                counter = counter+1
                if len(x) > 20:
                    x.pop(0)
                    y.pop(0)

                '''
                # Creazione del grafico
                plt.plot(x, y, '-o', label='Altezza acqua')
                plt.xlabel('last 20 measures')
                plt.ylabel('Altezza (cm)')
                plt.ylim(-2,10)

                # Salvataggio dell'immagine in memoria
                buf = BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)

                # Aggiornamento dell'immagine nella finestra
                plot_elem.update(data=buf.read())

                # Pulizia della figura di Matplotlib
                plt.clf()
                buf.close()
                '''
            elif dato[0] == "valve_value":
                print("Valvola: " + dato[1])
            else:
                print("Errore nella risposta del server")
    else:
        print(f"Errore nella richiesta HTTP. Codice di stato: {response.status_code}")
    
    root.after(100, myMainLoop)

root.after(100, myMainLoop)

# Avvia il loop principale della finestra
root.mainloop()
