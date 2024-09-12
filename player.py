import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
from dotenv import load_dotenv

load_dotenv()

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, open_browser=False))

# Shows playing devices
res = sp.devices()
pprint(res)

device = None
if len(res['devices']) > 0:
	print(f"Found device {res['devices'][0]['name']}")
	device = res['devices'][0]['id']

pprint(sp.me())

pprint(sp.currently_playing())

print("##############")

pprint(sp.current_user_playing_track())

# Change track
#sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])
#sp.start_playback(device_id=device, uris=['https://open.spotify.com/track/2bfGNzdiRa1jXZRdfssSzR'])

# Change volume
#sp.volume(100)
#sleep(2)
#sp.volume(50)
#sleep(2)
#sp.volume(100)
