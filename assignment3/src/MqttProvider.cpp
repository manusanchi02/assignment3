#include "MqttProvider.h"

WiFiClient espClient;
PubSubClient client(espClient);

MqttProvider::MqttProvider(char *mqtt_server, char *topic)
{
    this->mqtt_server = mqtt_server;
    this->topic = topic;
    wifiConnector = new WiFiConnector("iPhone di Emanuele", "11111111");
    wifiConnector->Connect();
}

void MqttProvider::Reconnect()
{

    // Loop until we're reconnected

    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");

        // Create a random client ID
        //String clientId = String("ESP32Client") + String(random(0xffff), HEX);

        // Attempt to connect
        if (client.connect("ESP32Client"))
        {
            Serial.println("connected");
            // Once connected, publish an announcement...
            // client.publish("outTopic", "hello world");
            // ... and resubscribe
            client.subscribe(topic);
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}
