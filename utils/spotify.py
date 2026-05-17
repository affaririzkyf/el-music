import re
import spotipy

from spotipy.oauth2 import (
    SpotifyClientCredentials
)


SPOTIFY_CLIENT_ID = "46f19bc2590a43f6acf8a4d06af4825e"
SPOTIFY_CLIENT_SECRET = "6ec409a045f843d79f88e2f4a2f35cb1"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
)

def is_spotify_url(url):

    return (
        "open.spotify.com/track/"
        in url
    )

def get_spotify_track(url):

    match = re.search(
        r"track/([A-Za-z0-9]+)",
        url
    )

    if not match:

        return None

    track_id = match.group(1)

    track = sp.track(track_id)

    title = track["name"]

    artist = track["artists"][0]["name"]

    return f"{title} {artist}"