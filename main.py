#!/usr/bin/env python

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from signal import pause
from dotenv import load_dotenv
import os
from time import sleep
from gpiozero import Button, TonalBuzzer

import rfid_readers

load_dotenv()

reader = rfid_readers.UIDFileReader()

MODE = 'play'
SAVE_DATA = ''

def button_callback():
    print("Button was pushed!")
    
    # playing = sp.current_user_playing_track()
    # if playing['currently_playing_type'] != 'track':
    #     print("Please play a track!")
    #     return

    # if playing['context'] == None:
    #     print("ERROR: No context")
    #     return

    global MODE, SAVE_DATA
    MODE = 'save'
    # SAVE_DATA = playing['context']['uri']
    
    buzzer.play('B4')
    sleep(0.2)
    buzzer.stop()

def main():
    global MODE, SAVE_DATA
    
    global sp
    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, open_browser=False))
    
    global button
    button = Button(os.getenv("BUTTON_PIN"))
    button.when_pressed = button_callback
    
    global buzzer
    buzzer = TonalBuzzer(os.getenv("BUZZER_PIN"))
    
    while True:
        print("Waiting to scan...")
        data = reader.read()
        print(f"Found card with data: {data}")
        
        if MODE == 'play':
            buzzer.play('C4')
            sleep(0.2)
            buzzer.stop()
        
            print("Playing data...")
            if data.startswith('spotify'):
                sp.start_playback(context_uri=data)
            else:
                print(f"Invalid card data \"{data}\"")

        elif MODE == 'save':
            print("Saving data...")
            
            playing = sp.current_user_playing_track()
            if playing['currently_playing_type'] != 'track':
                print("Please play a track!")
                return
            if playing['context'] == None:
                print("ERROR: No context")
                return
            SAVE_DATA = playing['context']['uri']
            
            print('press card')
            reader.write(SAVE_DATA)
            print("Data saved!")
            MODE = 'play'
            
            buzzer.play('C5')
            sleep(0.2)
            buzzer.stop()
            sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        reader.cleanup()
        print("Exiting...")
