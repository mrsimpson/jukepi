#!/usr/bin/env python
import sys
import time
import RPi.GPIO as GPIO
import os
from subprocess import call
from functools import partial

BUTTONS = []

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #we're referring to the pin numbers in order, not the GPIO IDs

# Map pins to functions
button = {'pin': 14, 'command': 'if volumio status | grep -q play; then volumio pause; else volumio play; fi'}
BUTTONS.append(button)

button = {'pin': 13, 'command': 'volumio next'}
BUTTONS.append(button)

button = {'pin': 11, 'command': 'volumio next'}
BUTTONS.append(button)

# We're using normal pushbuttons - if you use a rotary encoder, check the native volumio-plugin
button = {'pin': 31, 'command': 'volumio volume plus'}
BUTTONS.append(button)

button = {'pin': 29, 'command': 'volumio volume minus'}
BUTTONS.append(button)

def executeOs(command):
    os.system(button.command)

for button in BUTTONS:
    GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(button.pin, GPIO.RISING)
    GPIO.add_event_callback(button.pin, partial(executeOs, button.command))
