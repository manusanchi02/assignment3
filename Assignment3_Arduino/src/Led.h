#ifndef __LED__
#define __LED__
class Led
{
public:
    /**
     * Class contructor.
     * @param pin number of the pin where the led is connect.
     */
    Led(int pin);
    /**
     * Function to turn on the led.
     */
    void switchOn();
    /**
     * Function to turn off the led.
     */
    void switchOff();
    /**
     * Function to check if the is on.
     * @return true if on, false otherwise
     */
    bool isOn();

protected:
    int pin;
    bool state;
};
#endif