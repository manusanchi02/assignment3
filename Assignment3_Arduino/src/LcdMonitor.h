#ifndef __MONITOR__
#define __MONITOR__
#include <LiquidCrystal_I2C.h>
class LcdMonitor
{
public:
    /**
     * Class constructor.
     * @param rows number of rows to initialize
     * @param column number of rows to initialize
     */
    LcdMonitor(int rows, int columns);
    /**
     * Function to set a start position and print on the lcd monitor.
     * @param string what you want to print
     * @param xposition x coordinate of start pixel (0-based)
     * @param yposition y coordinate of start pixel (0-based)
     */
    void setAndPrint(String string, int xposition, int yposition);

    /**
     * Function to clean the lcd monitor.
    */
    void clean();

protected:
    LiquidCrystal_I2C *lcd;
};
#endif