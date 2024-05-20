from src.classes.spotify.spotify_client import SpotifyClient
from src.classes.data.DataManager import DataManager
from definitions import RAW_DATA_DIR

import os


# Creates a list of ids of the tracks
def get_track_ids(tracks):
    track_ids = []
    for item in tracks['items']:
        track_ids.append(item['track']['id'])

    return ','.join(track_ids)


# Creates a list of ids of the tracks
def get_artist_ids(tracks):
    artist_ids = set()
    for item in tracks['items']:
        artist = item['track']['artists'][0]
        artist_ids.add(artist['id'])

    return ','.join(artist_ids)


def main():
    spotify_client = SpotifyClient()

    # Fetch recently played tracks
    recently_played_tracks = spotify_client.get_recently_played_tracks()

    # Save recently played tracks to a file
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_recently_played_tracks.json")
    DataManager.save_to_json(raw_spotify_data_file, recently_played_tracks, overwrite=True)

    # Get ids of artists
    artist_ids = get_artist_ids(recently_played_tracks)

    # Fetch audio features of recently played tracks
    artist_information = spotify_client.get_several_artists(artist_ids)

    # Save artist information to a file
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_artist_information.json")
    DataManager.save_to_json(raw_spotify_data_file, artist_information, overwrite=True)

    # Get ids of recently played tracks
    track_ids = get_track_ids(recently_played_tracks)

    # Fetch audio features of recently played tracks
    track_audio_features = spotify_client.get_track_audio_features(track_ids)

    # Save track analysis to a file
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_track_features.json")
    DataManager.save_to_json(raw_spotify_data_file, track_audio_features, overwrite=True)


if __name__ == "__main__":
    main()
