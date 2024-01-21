/**
 * @author lorenzo.annibalini@studio.unibo.it 	Annibalini Lorenzo
 * @author lorenzo.bacchini4@studio.unibo.it 	Bacchini Lorenzo
 * @author emanuele.sanchi@studio.unibo.it 		Sanchi Emanuele
 */

#include "Button.h"
#include "Gate.h"
#include "LcdMonitor.h"
#include "Led.h"
#include <Arduino.h>
#include <EnableInterrupt.h>

#define LEDPIN1 10
#define LEDPIN2 11
#define LCDROWS 4
#define LCDCOLS 20
#define GATEPIN 13
#define GATEOPEN 180
#define GATECLOSE 0
#define BUTTONPIN 2

#define normalLevel 45
#define alarm_to_highLevel 90


Button *button;
Gate *gate;
LcdMonitor *lcd;
Led *ledGreen;
Led *ledRed;

int manualLevel=90;

volatile enum controllerState {
    normal,
    alarm_too_low,
    pre_alarm_too_high,
    alarm_too_high,
    alarm_too_high_critic,
    manual
} controllerState;

/**
 * Setup function, called once when the program starts.
 */
void setup()
{
	// calibrate sensors.
    button = new Button(BUTTONPIN);
    gate = new Gate(GATEPIN, GATEOPEN, GATECLOSE);
	lcd = new LcdMonitor(LCDROWS, LCDCOLS);
    ledGreen = new Led(LEDPIN1);
    ledRed = new Led(LEDPIN2);
	lcd->setAndPrint("Calibrating sensors", 0, 0);
    gate->setOpen();
    delay(1000);
    gate->setClose();
	delay(4000);

	Serial.begin(9600);
    controllerState = normal;
}

void setUnsetManualMode(){
    if(button->isPressed()){
        if(controllerState == manual){
            controllerState = normal;
        }else{
            controllerState = manual;
        }
    }
}

/**
 * Function called to make the fsm take a step forward over the controllerState.
*/
void step(){
    enableInterrupt(BUTTONPIN, setUnsetManualMode, CHANGE);
    /*
    int incomingByte = Serial.read();
    Serial.println("ciao",DEC);
    */
    //read data from River Monitoring Service (state and *level)
    //*level only if state sent is manual
    switch(controllerState){
        case normal:
            gate->setPos(normalLevel);
            break;
        case alarm_too_low:
            gate->setClose();
            break;
        case pre_alarm_too_high:
            gate->setPos(normalLevel);
            break;
        case alarm_too_high:
            gate->setPos(alarm_to_highLevel);
            break;
        case alarm_too_high_critic:
            gate->setOpen();
            break;
        case manual:
            map(manualLevel, 0, 100, 0, 180);
            gate->setPos(manualLevel);   
            break;
        default:
            Serial.println("Error: controllerState not valid");
            break;
    }
    lcd->clean();
    lcd->setAndPrint("Valve opening level:", 0, 0);
    lcd->setAndPrint(String(map(gate->getPos(), 0, 180, 0, 100))+"%", 0, 1);
    lcd->setAndPrint("current modality:", 0, 2);
    lcd->setAndPrint(((controllerState==manual) ? "manual" : "automatic"), 0, 3);
    //send data to River Monitoring Service (state and level)
}

/**
 * Loop function called continuously to make
 * the fsm take a step forward.
 */
void loop()
{
    step();
    delay(500);   
}