import time
import signal
import threading
import paho.mqtt.client as mqtt
from enum import Enum
import serial.tools.list_ports
from http.server import BaseHTTPRequestHandler, HTTPServer

#Enum per stati del sistema
class State(Enum):
    NORMAL = 0, "Normal"
    ALARM_TOO_LOW = 1, "Alarm too low"
    PRE_ALARM_TOO_HIGH = 2, "Pre-alarm too high"
    ALARM_TOO_HIGH = 3, "Alarm too high"
    ALARM_TOO_HIGH_CRITIC = 4, "Alarm too high critic"
    
    
print("stato1: " + str(State.NORMAL.value[1]))

#Costanti per valori frequenza
F1 = 1000
F2 = 500

#Costanti per valori soglia
WL1 = 1
WL2 = 2
WL3 = 4
WL4 = 5

# Impostazioni del broker MQTT
broker_address = "172.20.10.5"
server_port = 1883
topic_send = "frequency"
topic_receive = "water-level"

#impostazioni server HTTP


# Variabili globali
frequency_message = 0
valve_value = 0
water_level = 0
state = State.NORMAL
http_received = ""

# Classe che gestisce le richieste HTTP
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global state, water_level, valve_value

        try:
            #send code 200 response
            self.send_response(200)

            #send header first
            self.send_header('Content-type','text-html')
            self.end_headers()

            # Invia una risposta al client
            # get the state of the system with the string value of the enum
            
            message = "state:" + str(state.value[1]) + ";water_level:" + str(water_level) + ";valve_value:" + str(valve_value)
            #message = f"state:{state.value};water_level:{water_level};valve_value:{valve_value}"
            self.wfile.write(message.encode())
            return
        except IOError:
            self.send_error(404, 'errore')

# Funzione per avviare il server HTTP
def run():
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Server in ascolto sulla porta 8080")
    
    httpd.serve_forever()
    
    # Aggiungi la gestione del segnale di terminazione
    def handler(signum, frame):
        print("Ricevuto segnale di terminazione. Chiudo il server.")
        httpd.socket.close()

    signal.signal(signal.SIGINT, handler)



# Stampa delle porte seriali disponibili
print("Porte seriali disponibili:")
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print(f"{port}: {desc} [{hwid}]")

# Input utente per la porta seriale
selected_port = input("Inserisci il nome della porta seriale che vuoi utilizzare: ")

# Connessione alla porta seriale
#ser = serial.Serial(selected_port, 9600, timeout=1)
ser = serial.Serial()
ser.baudrate = 9600
ser.port = selected_port
ser.open()

# Callback che gestisce la connessione al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(topic_receive)
        print("Connesso al broker")
    else:
        print(f"Errore di connessione al broker, codice: {rc}")

# Funzione per inviare un messaggio al topic "frequency"
def publish_message(client, message):
    print(f"Invio messaggio: {message}")
    client.publish(topic_send, message)
    
# Callback che gestisce la ricezione di un messaggio
def on_message(client, userdata, msg):
    global water_level
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    water_level = float(msg.payload.decode())

# Creazione del client MQTT
client = mqtt.Client()

# Connessione al broker
client.connect(broker_address, server_port, 60)
client.subscribe(topic_receive)
client.on_message = on_message  # Set the on_message callback
client.loop_start()

# Avvio del server HTTP
http_thread = threading.Thread(target=run)
http_thread.start()


time.sleep(2)

# Loop principale
print(water_level)
try:
    while True:
        print(water_level)
        if(water_level < WL1):
            print("Livello acqua troppo basso")
            frequency_message = F1
            state = State.ALARM_TOO_LOW
            valve_value = 0
        if(water_level > WL1 and water_level < WL2):
            print("Livello acqua normale")
            frequency_message = F1
            state = State.NORMAL
            valve_value = 25
        if(water_level > WL2 and water_level <= WL3):
            print("Livello acqua troppo alto pre-allarme")
            frequency_message = F2
            state = State.PRE_ALARM_TOO_HIGH
            valve_value = 25
        if(water_level > WL3 and water_level <= WL4):
            print("Livello acqua troppo alto")
            frequency_message = F2
            state = State.ALARM_TOO_HIGH
            valve_value = 50
        if(water_level > WL4):
            print("Livello acqua troppo alto critico")
            frequency_message = F2
            state = State.ALARM_TOO_HIGH_CRITIC
            valve_value = 100
            
        # Invia un messaggio con la frequenza desiderata all'esp
        publish_message(client, frequency_message)
        
        # Invia messaggio ad Arduino
        msg = str(valve_value).encode()
        ser.write(msg)
        print("Serial: " + ser.readline().decode())

        # Attendi prima di inviare il prossimo messaggio
        time.sleep(frequency_message/1000)

except KeyboardInterrupt:
    print("Interruzione del loop infinito")
    client.disconnect()
    http_thread.join()