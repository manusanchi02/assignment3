#include <Arduino.h>
#include "Sonar.h"
#include "MqttProvider.h"
#include "Led.h"
#define CHANNEL_HEIGHT 5
#define SSID "iPhone di Emanuele"
#define PASSWORD "11111111"
#define SERVER "172.20.10.5"
#define TOPIC_WATER "water-level"
#define TOPIC_FREQ "frequency"
#define MQTT_PORT 1883
#define ECHO_PIN 13
#define TRIGGER_PIN 14
#define REDLEDPIN 4
#define GREENLEDPIN 5


// Electronics components
Sonar *sonar;
Led *redLed;
Led *greenLed;
// Mqtt
MqttProvider *mqttProvider;

char msg[MSG_BUFFER_SIZE];
int frequency;

void setup()
{
    Serial.begin(115200);
    sonar = new Sonar(ECHO_PIN, TRIGGER_PIN);
    redLed = new Led(REDLEDPIN);
    greenLed = new Led(GREENLEDPIN);
    redLed->switchOn();
    greenLed->switchOff();
    frequency = 0;
    mqttProvider = new MqttProvider(SSID, PASSWORD, SERVER, TOPIC_WATER, TOPIC_FREQ, MQTT_PORT);
    mqttProvider->setCallback(callback);
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
        greenLed->switchOff();
        redLed->switchOn();
        mqttProvider->reconnect();
        redLed->switchOff();
        greenLed->switchOn();
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
	if (strcmp(topic, TOPIC_FREQ) == 0) {
		Serial.print("valore ricevuto: ");
		frequency = byteArrayToInt(payload, length);
		Serial.println(frequency);
	}
}


