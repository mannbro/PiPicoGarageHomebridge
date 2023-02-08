import config
import network
import socket
import time
from uselect import select
from garagedoor import GarageDoor

garageDoor=GarageDoor(config.OPEN_SENSOR_PIN, config.CLOSED_SENSOR_PIN, config.TRIGGER_PIN, config.PULSE_LENGTH_MS, config.OBSTRUCTED_THRESHOLD_SECONDS)

def connectWifi():
    wifi.active(True)
    wifi.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    max_wait = 10
    while wifi.status() != 3:
        print('waiting for connection. Status: '+str(wifi.status()))
        time.sleep(1)

    print('connected')
    status = wifi.ifconfig()
    ipAddress=status[0]
    print( 'ip = ' + ipAddress )


def returnError(errcode):
    return '{"success": false, "error": "'+errcode+'"}'
    

#Handle an incoming request
def handleRequest(conn, address):
    request = conn.recv(1024)
    request = str(request)

    if request.find('/?open')==6:
        response=garageDoor.start(garageDoor.ACTION_OPEN)
    elif request.find('/?close')==6:
        response=garageDoor.start(garageDoor.ACTION_CLOSE)
    elif request.find('/?getstatus')==6:
        response=garageDoor.getStates()
    else:
        response=returnError('UNKNOWN_COMMAND')

    conn.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
    conn.send(response)
    conn.close()


wifi = network.WLAN(network.STA_IF)

connectWifi()

#Set up socket and start listening on port 80
addr = socket.getaddrinfo(wifi.ifconfig()[0], 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('listening on', addr)

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

