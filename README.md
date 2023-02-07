# PiPicoGarageHomebridge
Control a garage door using a Raspberry Pi Pico W, a relay, three resistors and Homebridge

# YouTube Video
To learn more, check out the YouTube video I made about the Garage Door Opener

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/-h3uSNCeCGY/0.jpg)](https://www.youtube.com/watch?v=-h3uSNCeCGY)

# Setting up the hardware
In order to control the door and detect if the door is opened or closed, we need to use three pins on the Raspberry Pi Pico.

The pins that I have chosen are:

Relay: Pin 21

Sensor to detect if the door is opened: Pin 19

Sensor to detect if the door is closed: Pin 20

The relay connects directly between Pin 21 and ground. The Impulse input is connected between COM and NO on the relay through a 180 Ohm resistor.

The Open and Closed sensors are connected to Pin 19 and 20 using 10k resistors.

# Installation on the Pi Pico

Make sure that you have Micropython installed on your Raspberry Pi Pico.

Edit the wifi setting in the main.py file and upload through your favourite tool, such as Thonny.

# Connecting to Homebridge

In order to connect the Pi Pico to Homebridge, I'm using the HTTP Advanced Accessory plugin by staromeste.

You can find the plugin here: https://github.com/staromeste/homebridge-http-advanced-accessory

This plugin is very powerful, but not very user friendly as it needs to be configured using JSON to talk to and understand accessories.

But don't despair. I included a working configuration file in this repository. Just copy and paste the contents into the plugin configuration. The only thing you need to do is replace "YOUR_PI_PICO" with the IP-address of your device.
