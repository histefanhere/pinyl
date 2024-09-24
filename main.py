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

class Buzzer:
    buzzer = None
    
    @staticmethod
    def init():
        Buzzer.buzzer = TonalBuzzer(os.getenv("BUZZER_PIN"))
        
    @staticmethod
    def beep(note):
        Buzzer.buzzer.play(note)
        sleep(0.2)
        Buzzer.buzzer.stop()
    
    @staticmethod
    def tone(note):
        Buzzer.buzzer.play(note)


class MyButton:
    button = None
    pressed = False

    @staticmethod
    def init():
        MyButton.button = Button(os.getenv("BUTTON_PIN"), bounce_time=0.2)
        MyButton.button.when_pressed = MyButton.button_callback

    @staticmethod
    def button_callback():
        print("Button was pushed!")
        MyButton.pressed = True
        Buzzer.beep('C5')


reader = rfid_readers.UIDFileReader()

def main():
    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, open_browser=False))
    
    MyButton.init()
    Buzzer.init()
    
    while True:
        print("Waiting to scan...")
        data = reader.read()
        print(f"Found card with data: {data}")
        
        if not MyButton.pressed:
            print("Playing data...")
            if data.startswith('spotify'):
                Buzzer.beep('C4')
                
                try:
                    sp.start_playback(context_uri=data)
                except spotipy.client.SpotifyException as e:
                    if 'NO_ACTIVE_DEVICE' in str(e):

                        print('No active device found, playing on any online device...')
                        devices = sp.devices()
                        if len(devices['devices']) == 0:
                            print('No devices found')
                        else:
                            device = devices['devices'][0]
                            print(f"Playing on {device['name']} ({device['type']})")

                            sp.start_playback(device_id=device['id'], context_uri=data)
                    else:
                        raise e
            else:
                print(f"Invalid card data \"{data}\"")

        else:
            print("Saving data...")
            
            Buzzer.tone('C4')
            
            playing = sp.current_user_playing_track()
            if playing['currently_playing_type'] != 'track':
                print("Please play a track!")
                return
            if playing['context'] == None:
                print("ERROR: No context")
                return
            
            print('press card')
            SAVE_DATA = playing['context']['uri']
            reader.write(SAVE_DATA)
            
            print("Data saved!")
            Buzzer.beep('C5')
        
        
        MyButton.pressed = False
        sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        reader.cleanup()
        print("Exiting...")
