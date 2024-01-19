#include "Gate.h"
#include <Arduino.h>
#define DELTA 1 // 1 degree


Gate::Gate(int pin, int open, int close)
{
    this->pin = pin;
    this->open = open;
    this->close = close;
    this->pos = 0;
    this->gateState = false;
}

void Gate::setOpen()
{
    this->pos = 0; // reset the position to 0
    if(!gateState) {
        this->servo.attach(pin);
        for(int i = 0; i < this->open; i++) {
            this->pos+=DELTA;
            this->servo.write(pos);
            delay(6); // small delay to permit the servo to reach the position
        }
        gateState = true;
        this->servo.detach();
    }
}

void Gate::setClose()
{
    this->pos = 90; // reset the position to 90
    if(gateState) {
        this->servo.attach(pin);
        for(int a = 0; a < this->open; a++) {
            this->pos-=DELTA;
            this->servo.write(pos);
            delay(6); // small delay to permit the servo to reach the position
        }
        gateState = false;
        this->servo.detach();
    }
}

void Gate::setPos(int degrees)
{
    int i;
    (degrees > pos) ? i=+1 : i=-1;
    this->servo.attach(pin);
    for(int a = 0; a < abs(degrees-pos); a++) {
        this->pos+=i;
        this->servo.write(pos);
        delay(6); // small delay to permit the servo to reach the position
    }
    degrees<90 ? gateState = false : gateState = true;
    this->servo.detach();
}

int Gate::getPos()
{
    return pos;
}

bool Gate::isOpen()
{
    return gateState;
}