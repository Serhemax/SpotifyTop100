from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open("needed_information", "r") as f:
    CLIENT_ID = f.readline()
    CLIENT_SECRET = f.readline()
    CLIENT_NAME = f.readline()

REDIRECT_URL = "http://localhost:3000"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=CLIENT_NAME,
    )
)
user_id = sp.current_user()["id"]
test = ['Incomplete', 'Bent', "It's Gonna Be Me", "Jumpin', Jumpin'", 'Try Again']


date = input("Which year do you what to travel to? Type the date in this format YYYY-MM-DD ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
web_page = response.text

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=date, public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

