#ifndef __MQTTPROV__
#define __MQTTPROV__
#include <WiFi.h>
#include <PubSubClient.h>
#include "WiFiConnector.h"
#define MSG_BUFFER_SIZE 50
class MqttProvider
{
public:
    /**
     * Constructor.
     * @param wifi-ssid: name of the wifi network
     * @param wifi-password: password of the wifi network
     * @param mqtt_server: name of the mqtt server
     * @param mqtt_topic_water: topic to publish water level
     * @param mqtt_topic_freq: topic to publish frequency
     * @param mqttport: port of the mqtt server
     */
    MqttProvider(char *wifi_ssid, char *wifi_password, char *mqtt_server, char *mqtt_topic_water, char *mqtt_topic_freq, int mqtt_port);
    /**
     * Function to reconnect;
     */
    void reconnect();

    /**
     * Function to get connection status.
     * @return true if the connection is up, false otherwaise
    */
    bool getConnStatus();

    /**
     * Function to send message via mqtt.
     * @param message: the string to send
    */
    void sendMessage(char* message);

    /**
     * Function to activate client loop.
    */
    void loop();

    /**
     * Function to set callback.
     * @param callback: the callback function
    */
    void setCallback(std::function<void (char *, uint8_t *, unsigned int)> callback);

private:
    char *mqtt_server;
    char *mqtt_topic_water;
    char *mqtt_topic_freq;
    int mqtt_port;
    WiFiConnector *wifiConnector;
    WiFiClient espClient;
    PubSubClient client;
};
#endif