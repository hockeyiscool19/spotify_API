import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import json
import pandas as pd
from sqlalchemy import create_engine, text
import os

# Retrieve POSTGRES_URI from environment variables
POSTGRES_URI = os.environ.get('POSTGRES_URI')


class RdsConnect:
    def __init__(self):
        self.engine = create_engine(POSTGRES_URI)
        self.conn = self.engine.connect()

    def execute(self, query):
        return pd.read_sql_query(text(query), con=self.conn)

    def write_df(self, df: pd.DataFrame, schema, name, if_exists):
        """if_exists: ['fail', 'replace', 'append']"""
        df.to_sql(name, self.conn, schema, index=True, if_exists=if_exists)
        print(f"Wrote {name} to {self.database}.{schema}")

    def end(self):
        self.conn.close()


# Set up authentication with Spotify API
username = os.environ.get('USERNAME')
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = os.environ.get('REDIRECT_URI')

scope = 'user-read-private user-read-email user-read-playback-state user-read-currently-playing user-modify-playback-state user-library-read user-library-modify user-top-read user-read-recently-played user-follow-read user-follow-modify'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                     client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Load JSON files
with open("data/Playlist1.json", encoding="utf8") as j:
    playlists = json.loads(j.read())

with open("data/SearchQueries.json", encoding="utf8") as j:
    searches = json.loads(j.read())

with open("data/StreamingHistory0.json", encoding="utf8") as j:
    streaming0 = json.loads(j.read())

with open("data/StreamingHistory1.json", encoding="utf8") as j:
    streaming1 = json.loads(j.read())

with open("data/YourLibrary.json", encoding="utf8") as j:
    library = json.loads(j.read())

# Function to format playlists data


def formatPlaylist(playlists=playlists):
    df = pd.DataFrame({})
    for play in playlists['playlists'][:]:
        playListName = play["name"]

        for song in play["items"]:
            track = song["track"]
            newDf = pd.DataFrame.from_dict(track, orient='index').T
            newDf["playlist"] = playListName
            df = pd.concat([df, newDf])
    return df

# Function to format streaming history data


def formatStreamingHistory(streaming0=streaming0, streaming1=streaming1):
    streaming0.extend(streaming1)
    return pd.DataFrame(streaming0)

# Function to format library data


def formatLibrary(library=library):
    return pd.DataFrame(library["tracks"])

# Function to extract top artists


def extract_top_artists(sp=sp):
    top_artists = sp.current_user_top_artists()
    top_artists_df = pd.DataFrame()
    for artist in top_artists['items']:
        artist_name = artist['name']
        artist_popularity = artist['popularity']
        artist_images = artist['images']
        artist_genres = artist['genres']
        artist_df = pd.DataFrame({'artist_name': [artist_name], 'artist_popularity': [
                                 artist_popularity], 'artist_images': [artist_images], 'artist_genres': [artist_genres]})
        top_artists
