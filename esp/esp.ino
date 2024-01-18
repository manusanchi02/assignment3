#include <Arduino.h>
#include "Sonar.h"
void setup() {
  Serial.begin(115200);
  //Serial.print("setup() is running on core ");
  //Serial.println(xPortGetCoreID());
  //delay(2000);
}

void loop() {
  //Serial.print("loop() is running on core ");
  //Serial.println(xPortGetCoreID());
  Sonar *sonar;
  //sonar.getDistance();
  Serial.println(sonar.getDistance());
  delay(1000);
}
