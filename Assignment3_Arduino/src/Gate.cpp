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
    this->setPos(open);
}

void Gate::setClose()
{
    this->setPos(close);
}

void Gate::setPos(int degrees)
{
    if(degrees != pos){
        int i;
        (degrees > pos) ? i=+DELTA : i=-DELTA;
        this->servo.attach(pin);
        int j = abs(degrees-pos);
        for(int a = 0; a < j; a++) {
            this->pos+=i;
            this->servo.write(pos);
            delay(6); // small delay to permit the servo to reach the position
        }
        degrees<open ? gateState = false : gateState = true;
        this->servo.detach();
    }
}

int Gate::getPos()
{
    return pos;
}

bool Gate::isOpen()
{
    return gateState;
}