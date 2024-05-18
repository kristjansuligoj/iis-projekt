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


def main():
    spotify_client = SpotifyClient()

    # Fetch recently played tracks
    recently_played_tracks = spotify_client.get_recently_played_tracks()

    # Save recently played tracks to a file
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_recently_played_tracks.json")
    DataManager.save_to_json(raw_spotify_data_file, recently_played_tracks, overwrite=True)

    # Get ids of recently played tracks
    track_ids = get_track_ids(recently_played_tracks)

    # Fetch audio features of recently played tracks
    track_audio_features = spotify_client.get_track_audio_features(track_ids)

    # Save track analysis to a file
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_track_features.json")
    DataManager.save_to_json(raw_spotify_data_file, track_audio_features, overwrite=True)


if __name__ == "__main__":
    main()
