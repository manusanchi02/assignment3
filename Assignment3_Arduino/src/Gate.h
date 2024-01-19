#ifndef __GATE__
#define __GATE__

#include <Servo.h>

class Gate
{
public:
    /**
     * Class contructor.
     * @param pin the pin number where the servo is connected.
     * @param open number of angular degrees to open the gate.
     * @param close number of angular degrees to close the gate.
    */
    Gate(int pin, int open, int close);
    /**
     * Function to open the gate.
    */
    void setOpen();
    /**
     * Function to close the gate.
    */
    void setClose();
    /**
     * Function to move gate to a specific position.
    */
    void setPos(int degrees);
    /**
     * Function to get the current position of the gate.
    */
    int getPos();
    /**
     * Function to check if the gate is open.
     * @return true if fully open, false otherwise
    */
    bool isOpen();

protected:
    int pin;
    int open;
    int close;
    int pos;
    bool gateState;
    Servo servo;
};
#endif