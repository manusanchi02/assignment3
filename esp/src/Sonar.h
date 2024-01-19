#ifndef __SONAR__
#define __SONAR__
class Sonar
{
public:
    /**
     * Class constructor.
     * @param echoPinIn number of the echo pin
     * @param trigPinOut number of the trig pin
     */
    Sonar(int echoPinIn, int trigPinOut);
    /**
     * Function to get the distance.
     */
    float getDistance();

protected:
    int echoPinIn;
    int trigPinOut;
};
#endif