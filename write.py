#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, open_browser=False))

reader = SimpleMFRC522()
try:
#	print("Waiting to scan...")
#	id, data = reader.read()
#	print(f"Found card with ID {id}")

	playing = sp.current_user_playing_track()
	if playing['currently_playing_type'] != 'track':
		print("Please play a track!")
		raise

	if playing['context'] == None:
		print("ERROR: No context")

	track_type = playing['context']['type']
	track_uri = playing['context']['uri']

	print(f"Waiting to save {track_type} to card...")
	id, data = reader.write(track_uri)

	print("Card ID:  ", id)
	print("Card Data:", data)
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
