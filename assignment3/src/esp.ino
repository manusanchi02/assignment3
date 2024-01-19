#include <Arduino.h>
#include "Sonar.h"
#include "MqttProvider.h"
#define CHANNEL_HEIGHT 10
Sonar *sonar;
MqttProvider *mqttProvider;
char msg[MSG_BUFFER_SIZE];
char *ssid = "iPhone di Emanuele";
char *password = "11111111";
char *server = "172.20.10.4"; // ip of the mqtt server (backend)
char *topic_water = "water-level";
char *topic_freq = "frequency";
int mqttport = 1883;
int frequency;
void setup()
{
    Serial.begin(115200);
    sonar = new Sonar(13, 14);
    // inizializzazione dei led
    frequency = 0;
    mqttProvider = new MqttProvider(ssid, password, server, topic_water, topic_freq, mqttport);
    mqttProvider->setCall(callback);
}

void loop()
{
    checkConnection();
    getAndSendWaterLevel();
    delay(frequency);
}

/**
 * Function to check if the connection is up.
*/
void checkConnection() {
    if(!mqttProvider->getConnStatus()) {
        //accensione e spegnimento dei led
        mqttProvider->Reconnect();
    }
    mqttProvider->loop();
}

/**
 * Function to get water level via sonar and send via mqtt.
*/
void getAndSendWaterLevel() {
	char message[10];
    float distance = sonar->getDistance();
    Serial.println(distance);
	int waterLevel = CHANNEL_HEIGHT - distance;
	sprintf(message, "%d", waterLevel);
	mqttProvider->sendMessage(message);
}

/**
 * Function to convert a byte array to int.
 * @param byteArray the byte array to convert.
 * @param size the size of the byte array.
*/
int byteArrayToInt(const unsigned char* byteArray, size_t size) {
    int result = 0;
    for (size_t i = 0; i < size; i++) {
        if (byteArray[i] >= '0' && byteArray[i] <= '9') {
            result = result * 10 + (byteArray[i] - '0');
        }
    }
    return result;
}

/**
 * Function to handle the callback.
 * @param topic the topic of the message.
 * @param payload the payload of the message.
 * @param length the length of the payload.
*/
void callback(char* topic, byte* payload, unsigned int length) {
	if (strcmp(topic, topic_freq) == 0) {
		Serial.print("valore ricevuto: ");
		frequency = byteArrayToInt(payload, length);
		Serial.println(frequency);
	}
}


