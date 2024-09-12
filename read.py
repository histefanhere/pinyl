#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, open_browser=False))

# Shows playing devices
res = sp.devices()
device = None
if len(res['devices']) > 0:
        print(f"Found device {res['devices'][0]['name']}")
        device = res['devices'][0]['id']

reader = SimpleMFRC522()
try:
	while True:
		print("Waiting to scan...")
		id, data = reader.read()
		data = data.strip()
		print("Card ID:  ", id)
		print("Card Data:", data)
		if data.startswith('spotify'):
			sp.start_playback(device_id=res['devices'][0]['id'], context_uri=data)
		else:
			print(f"Invalid card data \"{data}\"")

except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()

