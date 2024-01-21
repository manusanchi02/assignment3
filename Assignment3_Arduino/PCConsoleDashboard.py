import serial.tools.list_ports
import PySimpleGUI as sg


currentState = ''
levels = ''
comPort= 'COM3'

#Read COM port
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))

sg.theme('LightBlue')  # Add a touch of color
# All the stuff inside your window.
defaultLayout = [[sg.Text('Current State:') ,sg.Text(currentState,key='-STATE-')],
            [sg.Text('Opening level') ,sg.Text(levels,key='-LEVEL-')],
            [sg.Button('Maintenance done',key='-RESTART-', disabled=False)]]

loginLayout = [  [sg.Text('Please enter COM port')],
            [sg.Text('COM Port Available:'),sg.Text(*portsList)],
            [sg.Text('Enter the name:', size=(15, 1)), sg.InputText("COM3")],
            [sg.Button('Ok')]]

# Create the Window
windowLogin = sg.Window('Arduino Controller', loginLayout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = windowLogin.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        windowLogin.close()
        break
    if event == 'Ok':
        comPort = values[0]
        serialInst.baudrate = 9600
        serialInst.port = comPort
        serialInst.open()
        windowLogin.close()
        serialInst.write(b'prova:10')
        break

window = sg.Window('Arduino Controller', defaultLayout)
while True:
    
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        window.close()
        break

    if serialInst.in_waiting:
        packet = serialInst.readline()       
        msg = packet.decode('utf').rstrip('\n')
        if(msg.split(':')[0] == "0"):
            currentState = "normal"
            window['-STATE-'].update(currentState) 
            levels = msg.split(':')[1]
            window['-LEVEL-'].update(levels)
        elif(msg.split(':')[0] == "5"):
            currentState = "manual"
            window['-STATE-'].update(currentState)
            levels = msg.split(':')[1]
            window['-LEVEL-'].update(levels)
        else:
            currentState = msg.split(':')[0]
            window['-STATE-'].update(currentState)
            levels = msg.split(':')[1]
            window['-LEVEL-'].update(levels)
            
    if event == "-RESTART-":
        serialInst.write(b'prova:10')

        
window.close()