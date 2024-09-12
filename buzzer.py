#!/usr/bin/env python
""" Test script that plays a tone on a buzzer connected to GPIO 20. """

from gpiozero import TonalBuzzer
from time import sleep

buzzer = TonalBuzzer(20)

buzzer.play('A3')
sleep(1)
buzzer.play('E4')
sleep(1)
buzzer.stop()
