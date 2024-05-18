from src.classes.data.DataManager import DataManager
from definitions import RAW_DATA_DIR

import pandas as pd
import json
import os


def create_df_recently_played():
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_recently_played_tracks.json")

    # Read data from the JSON file
    with open(raw_spotify_data_file, "r") as json_file:
        data = json.load(json_file)

    rows = []
    for item in data['items']:
        track = item['track']

        row = {
            'artists': track['artists'][0]['name'],
            'duration': track['duration_ms'],
            'explicit': track['explicit'],
            'name': track['name'],
            'popularity': track['popularity'],
            'played_at': item['played_at'],
        }

        rows.append(row)

    return pd.DataFrame(rows)


def create_df_track_features():
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_track_features.json")

    # Read data from the JSON file
    with open(raw_spotify_data_file, "r") as json_file:
        data = json.load(json_file)

    rows = []
    for item in data['audio_features']:
        row = {
            'danceability': item['danceability'],
            'energy': item['energy'],
            'key': item['key'],
            'loudness': item['loudness'],
            'mode': item['mode'],
            'speechiness': item['speechiness'],
            'acousticness': item['acousticness'],
            'instrumentalness': item['instrumentalness'],
            'liveness': item['liveness'],
            'valence': item['valence'],
            'tempo': item['tempo'],
            'id': item['id'],
        }

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    df_recently_played = create_df_recently_played()
    df_track_features = create_df_track_features()

    df = pd.concat([df_recently_played, df_track_features], axis=1)
    df = df.drop(columns='id')

    column_rename_mapping = {
        'duration': 'length',
        'played_at': 'date',
    }

    # Create a new dictionary with the renamed columns
    df = df.rename(columns=column_rename_mapping)

    # Transform to datetime
    df['date'] = pd.to_datetime(df['date'], format='ISO8601')

    # Convert the normalized datetimes back to strings in the desired format
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    df = df.sort_values(by='date', ascending=True)

    processed_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "preprocessed_spotify_data.csv")
    DataManager.save_to_csv(processed_spotify_data_file, df, overwrite=True)


if __name__ == "__main__":
    main()
