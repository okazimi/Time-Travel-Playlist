import os
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

# ASK USER FOR INPUT
DATE = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
YEAR = DATE.split("-")[0]

# RETRIEVE BILLBOARDS TOP 100 SONGS FOR THAT DATE
response = requests.get(url="https://www.billboard.com/charts/hot-100/" + DATE)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
songs_span = soup.find_all(name="span", class_="chart-element__information__song")
songs = [song.getText() for song in songs_span]

# AUTHENTICATE SPOTIFY ACCOUNT
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="https://open.spotify.com/collection/playlists",
        scope="playlist-modify-private",
        cache_path="token.txt",
        show_dialog=True,
        )
    )

user_id = os.environ["USER_ID"]

# OBTAIN SONG URI'S
song_uris = []
for song in songs:
    result = sp.search(q=f"track:{song} year:{YEAR}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"The song {song} does not exist in Spotify's library and has been skipped.")


# CREATE PLAYLIST
playlist = sp.user_playlist_create(user=user_id, name=f"The Day We Met💑 ", public=False, collaborative=False, description=f"Top 100 hits from the day I met the love of my life🧡💛")
add_tracks = sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


