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
void setUnsetManualMode();

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
String data;
String state;

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

    enableInterrupt(BUTTONPIN, setUnsetManualMode, CHANGE);
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

String readStringFromSerial(){
    String inputString = "";
    char incomingByte;

    while (Serial.available() > 0) {
        // Leggi il carattere successivo
        Serial.readBytes(&incomingByte, 1);
        // Aggiungi il carattere alla stringa di input
        inputString += incomingByte;
    }
    return inputString;
}

String splitString(char separator, int index, String data){
    int found = 0;
    int strIndex[] = {0, -1};
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i + 1 : i;
        }
    }

    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

enum controllerState getNewState(){
    state = splitString(':', 0, data);
    if(state == "normal"){
        return normal;
    }else if(state == "alarm_too_low"){
        return alarm_too_low;
    }else if(state == "pre_alarm_too_high"){
        return pre_alarm_too_high;
    }else if(state == "alarm_too_high"){
        return alarm_too_high;
    }else if(state == "alarm_too_high_critic"){
        return alarm_too_high_critic;
    }else if(state == "manual"){
        manualLevel = map(splitString(':', 1, data).toInt(), 0, 100, 0, 180);
        return manual;
    }
}

/**
 * Function called to make the fsm take a step forward over the controllerState.
*/
void step(){
    //read data from River Monitoring Service (state and *level)
    //*level only if state sent is manual
    data = readStringFromSerial();
    if(data.length() > 0 && controllerState != manual){
        controllerState = getNewState();
    }
    
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
    Serial.println((String)controllerState + ":" + String(map(gate->getPos(), 0, 180, 0, 100))+"%");
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