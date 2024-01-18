#ifndef __MQTTPROV__
#define __MQTTPROV__
#include <WiFi.h>
#include <PubSubClient.h>
#include "WiFiConnector.h"
#define MSG_BUFFER_SIZE  50
class MqttProvider
{
public:
    /**
     * @param mqtt_server: name of the mqtt server
     * @param topic: topic to publish
    */
    MqttProvider(char* mqtt_server, char* topic);
    /**
     * Function to reconnect;
     */
    void Reconnect();

    PubSubClient GetClient() { return client; }

protected:
    char* mqtt_server;
    char* topic;
    WiFiConnector* wifiConnector;
    PubSubClient client;
};
#endif