import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

def update_graph(i, ax, line, x):
    # Aggiorna il grafico con nuovi dati (esempio)
    new_y = np.sin(x + i / 10.0)
    line.set_ydata(new_y)
    return line,

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def main():
    sg.theme("LightBlue1")

    # Dati del grafico (esempio)
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Creazione del layout della GUI
    layout = [
        [sg.Canvas(key='-CANVAS-', size=(400, 400))],
        [sg.Button("Esci")]
    ]

    # Creazione della finestra
    window = sg.Window("Grafico con PySimpleGUI", layout, resizable=True, finalize=True)

    # Creazione del grafico iniziale
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    line, = ax.plot(x, y)
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    # Funzione di aggiornamento per l'animazione
    update_func = lambda i: update_graph(i, ax, line, x)

    # Creazione dell'animazione che si aggiorna ogni secondo
    animation = FuncAnimation(fig, update_func, interval=1000, blit=False)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Esci":
            break

    window.close()

if __name__ == "__main__":
    main()
