#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO
import os
from subprocess import call
from functools import partial

class Button:
    def __init__(self, pin, command):
	self.pin = pin
	self.command = command

BUTTONS = []

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #we're referring to the GPIO IDs, not the sequence numbers

# Map pins to functions
playBtn = Button(22, 'if volumio status | grep -q play; then volumio pause; else volumio play; fi')
BUTTONS.append(playBtn)

nextBtn = Button(23, 'volumio next')
BUTTONS.append(nextBtn)

prevBtn = Button(17, 'volumio previous')
BUTTONS.append(prevBtn)

# We're using normal pushbuttons - if you use a rotary encoder, check the native volumio-plugin
volumeUpBtn = Button(5, 'volumio volume plus')
BUTTONS.append(volumeUpBtn)

volumeDownBtn = Button(6, 'volumio volume minus')
BUTTONS.append(volumeDownBtn)

def executeOs(command, pin): #we have to pass the pin as second argument since it will be passed by the caller anyway
    #print("executing " + command)
    os.system(command)

def trace(pin):
	print pin, "pushed"

for button in BUTTONS:
    print "BCM pin", button.pin, "setup to execute", button.command
    GPIO.setup(button.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(button.pin, GPIO.RISING, callback=partial(executeOs, button.command), bouncetime=250)

try:  
    while True: 
	    time.sleep(1)
except:
    GPIO.cleanup()