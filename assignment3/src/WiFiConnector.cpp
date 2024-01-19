#include "WiFiConnector.h"

WiFiConnector::WiFiConnector(char *ssid, char *password)
{
    this->ssid = ssid;
    this->password = password;
}

void WiFiConnector::Connect()
{
    delay(10);

    Serial.println(String("Connecting to ") + ssid);

    //WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}