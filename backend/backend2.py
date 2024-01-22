import time
import paho.mqtt.client as mqtt
from enum import Enum

#Enum per stati del sistema
class State(Enum):
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
state = State.NORMAL

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

# Loop principale
print(water_level)
try:
    while True:
        print(water_level)
        if(water_level < WL1):
            print("Livello acqua troppo basso")
            frequency_message = F1
            state = State.ALARM_TOO_LOW.value
            valve_value = 0
        if(water_level > WL1 and water_level < WL2):
            print("Livello acqua normale")
            frequency_message = F1
            state = State.NORMAL.value
            valve_value = 25
        if(water_level > WL2 and water_level <= WL3):
            print("Livello acqua troppo alto pre-allarme")
            frequency_message = F2
            state = State.PRE_ALARM_TOO_HIGH.value
            valve_value = 25
        if(water_level > WL3 and water_level <= WL4):
            print("Livello acqua troppo alto")
            frequency_message = F2
            state = State.ALARM_TOO_HIGH.value
            valve_value = 50
        if(water_level > WL4):
            print("Livello acqua troppo alto critico")
            frequency_message = F2
            state = State.ALARM_TOO_HIGH_CRITIC.value
            valve_value = 100
            
        # Invia un messaggio con la frequenza desiderata all'esp
        publish_message(client, frequency_message)

        # Attendi prima di inviare il prossimo messaggio
        time.sleep(frequency_message/1000)

except KeyboardInterrupt:
    print("Interruzione del loop infinito")
    client.disconnect()