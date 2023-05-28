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
        top_artists_df = top_artists_df.append(artist_df)

    top_artists_df['image_url'] = top_artists_df["artist_images"].apply(
        lambda x: x[0]['url'])
    top_artists_df = top_artists_df.drop(columns=['artist_images'])

    return top_artists_df


def extract_top_tracks(sp=sp):
    top_tracks = sp.current_user_top_tracks()
    top_tracks_df = pd.DataFrame()
    for track in top_tracks['items']:
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']
        popularity = track['popularity']
        images = track['album']['images']
        uri = track['uri']
        track_number = track['track_number']
        track_df = pd.DataFrame({'track_name': [track_name], 'artist_name': [artist_name], 'album_name': [
                                album_name], 'popularity': [popularity], 'images': [images], 'uri': [uri], 'track_number': [track_number]})
        top_tracks_df = top_tracks_df.append(track_df)

    top_tracks_df['audio_features'] = top_tracks_df['uri'].apply(
        lambda x: sp.audio_features(x))
    top_tracks_df['danceability'] = top_tracks_df['audio_features'].apply(
        lambda x: x[0]['danceability'])
    top_tracks_df['energy'] = top_tracks_df['audio_features'].apply(
        lambda x: x[0]['energy'])
    top_tracks_df['key'] = top_tracks_df['audio_features'].apply(
        lambda x: x[0]['key'])
    top_tracks_df['loudness'] = top_tracks_df['audio_features'].apply(
        lambda x: x[0]['loudness'])
    top_tracks_df['mode'] = top_tracks_df['audio_features'].apply(
        lambda x: x[0]['mode'])
    top_tracks_df['speechiness'] = top_tracks_df['audio_features'].apply(
        lambda x: x[0]['speechiness'])
    top_tracks_df['acousticness'] = top_tracks_df['audio_features'].apply(
        lambda x: x[0]['acousticness'])
    top_tracks_df['image_url'] = top_tracks_df['images'].apply(
        lambda x: x[0]['url'])
    top_tracks_df.drop(columns=['images'], inplace=True)
    top_tracks_df.drop(columns=['audio_features'], inplace=True)
    return top_tracks_df


def main():
    playlist = formatPlaylist()
    streaming_history = formatStreamingHistory()
    lib = formatLibrary()

    top_artists = extract_top_artists()
    top_tracks = extract_top_tracks()

    rds = RdsConnect()

    rds.write_df(playlist, "public", "playlists", "replace")
    rds.write_df(lib, "public", "library", "replace")
    rds.write_df(streaming_history, "public", "streaming_history", "replace")

    rds.write_df(top_artists, "public", "top_artists", "replace")
    rds.write_df(top_tracks, "public", "top_tracks", "replace")

    rds.end()

