#include <Arduino.h>
#include "Sonar.h"
#include "MqttProvider.h"

Sonar *sonar;
MqttProvider *mqttProvider;
unsigned long lastMsgTime = 0;
char msg[MSG_BUFFER_SIZE];
int value = 0;
char *topic = "esiot-2023";
void setup()
{
    Serial.begin(115200);
    sonar = new Sonar(13, 14);
    mqttProvider = new MqttProvider("broker.mqtt-dashboard.com", topic);
}

void loop()
{
    float distance = sonar->getDistance();
    Serial.println(distance);
    delay(1000);
    PubSubClient client = *mqttProvider->GetClient();
    if (!client.connected())
    {
        mqttProvider->Reconnect();
    }
    client.loop();

    unsigned long now = millis();
    if (now - lastMsgTime > 10000)
    {
        lastMsgTime = now;
        value++;

        /* creating a msg in the buffer */
        snprintf(msg, MSG_BUFFER_SIZE, "hello world #%ld", value);

        Serial.println(String("Publishing message: ") + msg);

        /* publishing the msg */
        client.publish(topic, msg);
    }
}
