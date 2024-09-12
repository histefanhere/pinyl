#!/usr/bin/env python
""" Test script for a button connected to GPIO 16 """

from gpiozero import Button
from signal import pause

button = Button(16, bounce_time=0.1)

def button_pressed():
    print("Button pressed")

button.when_pressed = button_pressed

pause()
