import threading
import time
import paho.mqtt.client as mqtt
import serial.tools.list_ports
from http.server import BaseHTTPRequestHandler, HTTPServer

#Enum per stati del sistema
class State:
    NORMAL = 0
    ALARM_TOO_LOW = 1
    PRE_ALARM_TOO_HIGH = 2
    ALARM_TOO_HIGH = 3
    ALARM_TOO_HIGH_CRITIC = 4

#Costanti per valori frequenza
F1 = 1000
F2 = 500

#Costanti per valori soglia
WL1 = 2
WL2 = 5
WL3 = 7
WL4 = 10

# Impostazioni del broker MQTT
broker_address = "172.20.10.5"
server_port = 1883
topic_send = "frequency"
topic_receive = "water-level"

# Variabili globali
frequency_message = 0
valve_value = 0
water_level = 0
State = State.NORMAL
http_received = ""

water_level_lock = threading.Lock()

# Classe che gestisce le richieste HTTP
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/send_data':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            content_length = int(self.headers['Content-Length'])
            http_received = self.rfile.read(content_length).decode('utf-8')

            message = "state:" + str(State) + ";water_level:" + str(water_level) + ";valve_value:" + str(valve_value)
            self.wfile.write(message.encode())
            return

# Funzione per avviare il server HTTP
def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server in ascolto sulla porta {port}")
    httpd.serve_forever()

# Stampa delle porte seriali disponibili
print("Porte seriali disponibili:")
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print(f"{port}: {desc} [{hwid}]")

# Input utente per la porta seriale
selected_port = input("Inserisci il nome della porta seriale che vuoi utilizzare: ")

# Connessione alla porta seriale
ser = serial.Serial(selected_port, 115200, timeout=1)

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
    with water_level_lock:
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        water_level = float(msg.payload.decode())

# Creazione del client MQTT
client = mqtt.Client()

# Connessione al broker
client.connect(broker_address, server_port, 60)
client.subscribe(topic_receive)
client.on_message = on_message  # Set the on_message callback

# Start the MQTT loop in a separate thread
mqtt_thread = threading.Thread(target=client.loop_forever)
mqtt_thread.start()

# Avvio del server HTTP
http_thread = threading.Thread(target=run)
http_thread.start()


# Loop principale
print(water_level)
try:
    while True:
        with water_level_lock:
            print(water_level)
            if(water_level < WL1):
                print("Livello acqua troppo basso")
                frequency_message = F1
                State = 1
                valve_value = 0
            if(water_level > WL1 and water_level < WL2):
                print("Livello acqua normale")
                frequency_message = F1
                State = State.NORMAL
                valve_value = 25
            if(water_level > WL2 and water_level <= WL3):
                print("Livello acqua troppo alto pre-allarme")
                frequency_message = F2
                State = State.PRE_ALARM_TOO_HIGH
                valve_value = 25
            if(water_level > WL3 and water_level <= WL4):
                print("Livello acqua troppo alto")
                frequency_message = F2
                State = State.ALARM_TOO_HIGH
                valve_value = 50
            if(water_level > WL4):
                print("Livello acqua troppo alto critico")
                frequency_message = F2
                State = State.ALARM_TOO_HIGH_CRITIC
                valve_value = 100
                
            # Invia un messaggio con la frequenza desiderata all'esp
            publish_message(client, frequency_message)
            
            # Invia messaggio ad Arduino
            msg = str(valve_value).encode()
            #ser.write(msg)

            # Attendi prima di inviare il prossimo messaggio
            time.sleep(frequency_message/1000)

except KeyboardInterrupt:
    print("Interruzione del loop infinito")
    client.disconnect()
