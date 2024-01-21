import time
import paho.mqtt.client as mqtt

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

# Impostazioni del broker MQTT
broker_address = "172.20.10.4"
topic_send = "frequency"
topic_receive = "state"
frequency_message = 100

# Callback che gestisce la connessione al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connesso al broker")
    else:
        print(f"Errore di connessione al broker, codice: {rc}")

# Funzione per inviare un messaggio al topic "frequency"
def publish_message(client, message):
    print(f"Invio messaggio: {message}")
    client.publish(topic, message)

# Creazione del client MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Connessione al broker
client.connect(broker_address, 1883, 60)

# Loop principale
try:
    while True:
        # Invia un messaggio con la frequenza desiderata
        publish_message(client, frequency_message)

        # Attendi prima di inviare il prossimo messaggio
        time.sleep(1)
        frequency_message+=100

except KeyboardInterrupt:
    print("Interruzione del loop infinito")
    client.disconnect()
