#WiFi Configuration
WIFI_SSID = 'XXXXX'
WIFI_PASSWORD = 'XXXXX'

#Pin for door open sensor
OPEN_SENSOR_PIN=19

#Pin for door closed sensor
CLOSED_SENSOR_PIN=20

#Pin for trigger to start door
TRIGGER_PIN=21

#How long pulse to send to start the door
PULSE_LENGTH_MS=500

#After how long time should we consider the door obstructed/stuck?
#Should be as long it takes to open or close the door (whichever takes longer),
#plus a few seconds as margin
OBSTRUCTED_THRESHOLD_SECONDS=40
