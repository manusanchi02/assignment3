import requests
import time
time.sleep(2)  # Attendi 1 secondo (puoi regolare il valore se necessario)
url = 'http://localhost:8080'  # Aggiorna la porta se necessario
response = requests.get(url)

if response.status_code == 200:
    print("Risposta del server:", response.text)
else:
    print("Errore nella richiesta:", response.status_code)