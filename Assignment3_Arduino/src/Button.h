#ifndef __BUTTON__
#define __BUTTON__
class Button
{
public:
    /**
     * Class contructor.
     * @param pin the pin number where button is connected.
     */
    Button(int pin);
    /**
     * Function to check if a button is pressed.
     */
    bool isPressed();

protected:
    int pin;
};
#endif