#include "MqttProvider.h"

MqttProvider::MqttProvider(char* wifi_ssid, char* wifi_password, char* mqtt_server, char* mqtt_topic_water, char *mqtt_topic_freq, int mqtt_port): espClient(), client(espClient) 
{
    this->mqtt_server = mqtt_server;
    this->mqtt_topic_water = mqtt_topic_water;
    this->mqtt_topic_freq = mqtt_topic_freq;
    wifiConnector = new WiFiConnector(wifi_ssid, wifi_password);
    wifiConnector->connect();
    this->client.setServer(mqtt_server, mqtt_port);
}

void MqttProvider::reconnect()
{

    // Loop until we're reconnected

    while (!this->client.connected())
    {
        if (WiFi.status() != WL_CONNECTED) {
            wifiConnector->connect();
        }
        Serial.print("Attempting MQTT connection...");
        delay(1000);
        // Attempt to connect
        if (this->client.connect("ESP32Client"))
        {
            Serial.println("connected");
            this->client.subscribe(this->mqtt_topic_freq);
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(this->client.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

bool MqttProvider::getConnStatus() {
    return this->client.connected() && WiFi.status() == WL_CONNECTED;
}

void MqttProvider::sendMessage(char* message) {
    Serial.println("Sending message: " + String(message));
    this->client.publish(this->mqtt_topic_water, message);
}

void MqttProvider::loop() {
    this->client.loop();
}

void MqttProvider::setCallback(std::function<void (char *, uint8_t *, unsigned int)> callback) {
    this->client.setCallback(callback);
}