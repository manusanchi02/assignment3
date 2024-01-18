#include <Arduino.h>
#include "Sonar.h"

Sonar *sonar;
void setup()
{
    Serial.begin(115200);
    sonar = new Sonar(13, 14);
    Serial.println("setup");
}

void loop()
{
    Serial.println(sonar->getDistance());
    delay(1000);
}
