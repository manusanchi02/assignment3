#ifndef __WIFI__
#define __WIFI__
#include <WiFi.h>
class WiFiConnector
{
public:
    /**
     * @param ssid: name of the network
     * @param password: password of the network
    */
    WiFiConnector(char* ssid, char* password);
    /**
     * Function to connect to the network.
     */
    void connect();

protected:
    char* ssid;
    char* password;
};
#endif