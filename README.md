# PiPicoGarageHomebridge
Control a garage door using a Raspberry Pi Pico and Homebridge

# YouTube Video

A YouTube video with a walkthrough of the hardware, the software and my setup will be available shortly.

# Setting up the hardware
In order to control the door and detect if the door is opened or closed, we need to use three pins on the Raspberry Pi Pico.

The pins that I have chosen are:

Relay: Pin 21
Sensor to detect if the door is opened: Pin 20
Sensor to detect if the door is closed: Pin 19

The relay connects directly between Pin 21 and ground. The Impulse input is connected between COM and NO on the relay through a 180 Ohm resistor.

The Open and Closed sensors are connected to Pin 19 and 20 using 10k resistors.

# Installation on the Pi Pico

Make sure that you have Micropython installed on your Raspberry Pi Pico.

Edit the wifi setting in the main.py file and upload through your favourite tool, such as Thonny.

# Connecting to Homebridge

In order to connect the Pi Pico to Homebridge, I'm using the HTTP Advanced Accessory plugin by staromeste.

This plugin is very powerful, but not very user friendly as it needs to be configured using JSON so that it can talk to and understand the accessory.

A working configuration file is included in this repository. Just copy and paste the contents into the plugin configuration. The only thing you need to do is replace YOUR_PI_PICO with the IP-address of your device.
