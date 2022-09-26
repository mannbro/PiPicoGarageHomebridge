import network
import socket
import time
from uselect import select
from machine import Pin


#Set up pins
CLOSED_PIN=19
OPEN_PIN=20
RELAY_PIN=21

#Pulse length in ms
PULSE_LENGTH=500

#Homekit target and current states
TARGET_DOOR_STATE_OPEN=0
TARGET_DOOR_STATE_CLOSED=1
CURRENT_DOOR_STATE_OPEN = 0;
CURRENT_DOOR_STATE_CLOSED = 1;
CURRENT_DOOR_STATE_OPENING = 2;
CURRENT_DOOR_STATE_CLOSING = 3;
CURRENT_DOOR_STATE_STOPPED = 4;

#Set initial target and current states
targetState=TARGET_DOOR_STATE_CLOSED
currentState=CURRENT_DOOR_STATE_CLOSED

#Setup pins for relay and sensors
relay = Pin(RELAY_PIN, Pin.OUT)
openSensor=Pin(OPEN_PIN, Pin.IN, Pin.PULL_UP)
closedSensor=Pin(CLOSED_PIN, Pin.IN, Pin.PULL_UP)

wifi = network.WLAN(network.STA_IF)


def connectWifi():
    global wlan

    ssid = 'XXXXXXXX'
    password = 'XXXXXXXX'

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    max_wait = 10
    while wifi.status() != 3:
        print('waiting for connection. Status: '+str(wifi.status()))
        time.sleep(1)

    print('connected')
    status = wifi.ifconfig()
    ipAddress=status[0]
    print( 'ip = ' + ipAddress )

connectWifi()

#Set up socket and start listening on port 80
addr = socket.getaddrinfo(wifi.ifconfig()[0], 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('listening on', addr)

def startDoor(newTargetState):
    global targetState
    global currentState
    
    targetState=newTargetState


    print('startDoor', targetState, currentState)

    relay.value(1)
    time.sleep_ms(PULSE_LENGTH)
    relay.value(0)

    setCurrentState()

    return getDoorStatus()

def setCurrentState():
    global targetState
    global currentState    
    global openSensor
    global closedSensor

    print("openSensor", openSensor.value())
    print("closedSensor", closedSensor.value())
    
    if(openSensor.value()==0):
        currentState=CURRENT_DOOR_STATE_OPEN
        targetState=TARGET_DOOR_STATE_OPEN
    elif(closedSensor.value()==0):
        currentState=CURRENT_DOOR_STATE_CLOSED
        targetState=TARGET_DOOR_STATE_CLOSED
    elif targetState==TARGET_DOOR_STATE_OPEN:
        currentState=CURRENT_DOOR_STATE_OPENING
    elif targetState==TARGET_DOOR_STATE_CLOSED:
        currentState=CURRENT_DOOR_STATE_CLOSING
    else:
        currentState=CURRENT_DOOR_STATE_STOPPED

def getDoorStatus():
    global targetState
    global currentState

    #Ensure current state is up to date
    setCurrentState()

    print('getDoorStatus', targetState, currentState)
    return '{"success": true, "currentState": '+str(currentState)+', "targetState": '+str(targetState)+'}'

def returnError(errcode):
    print('returnError')
    return '{"success": false, "error": "'+errcode+'"}'
    

#Handle an incoming request
def handleRequest(conn, address):
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)

    print(request)

    if request.find('/?open')==6:
        response=startDoor(TARGET_DOOR_STATE_OPEN)
    elif request.find('/?close')==6:
        response=startDoor(TARGET_DOOR_STATE_CLOSED)
    elif request.find('/?getstatus')==6:
        response=getDoorStatus()
    else:
        response=returnError('UNKNOWN_COMMAND')

    conn.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
    conn.send(response)
    conn.close()

#Main Loop
while True:
    #Check if wifi is connected, if not, reconnect
    if wifi.isconnected() == False:
        print('Connecting wifi...')
        connectWifi()

    #Handle incoming HTTP requests in a non-blocking way
    r, w, err = select((s,), (), (), 1)

    #Is there an incoming request? If so, handle the request
    if r:
        for readable in r:
            conn, addr = s.accept()
            try:
                handleRequest(conn, addr)
            except OSError as e:
                pass
