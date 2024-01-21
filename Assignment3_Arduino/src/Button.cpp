#include "Button.h"
#include <Arduino.h>
#define FIXAMOUNT 200

long previousTime;

Button::Button(int pin)
{
    this->pin = pin;
    previousTime = millis();
    pinMode(pin, INPUT);
}

/**
 * Function to resolve phisical bouncing of a button.
*/
bool resolveBouncing()
{
    if (millis() - previousTime > FIXAMOUNT)
    {
        previousTime = millis();
        return true;
    }
    return false;
}

bool Button::isPressed()
{
    return resolveBouncing() && digitalRead(pin) == HIGH;
}