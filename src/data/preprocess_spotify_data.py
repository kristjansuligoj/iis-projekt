from src.classes.data.DataManager import DataManager
from definitions import RAW_DATA_DIR

import pandas as pd
import json
import os


def simplify_genre(genres):
    # Genre mappings
    genre_mappings = {
        'classical': 'classical',
        'hip hop': 'hip hop',
        'pop': 'pop',
        'rap': 'rap',
        'metal': 'metal',
        'country': 'country',
        'lo-fi': 'lo-fi',
        'indie': 'indie',
        'rock': 'rock',
    }

    # Iterate through the provided genres
    general_genre = ""
    for genre in genres:
        # Check if the genre matches any of the mappings exactly
        if genre.lower() in genre_mappings:
            general_genre = genre_mappings[genre.lower()]

        else:
            # Check if any mapping is a substring of the genre
            for mapping in genre_mappings:
                if mapping in genre.lower():
                    general_genre = genre_mappings[mapping]
                    break  # Stop searching for mappings if a match is found

    return general_genre


def create_df_recently_played():
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_recently_played_tracks.json")

    # Read data from the JSON file
    with open(raw_spotify_data_file, "r") as json_file:
        data = json.load(json_file)

    rows = []
    for item in data['items']:
        track = item['track']

        row = {
            'artist': track['artists'][0]['name'],
            'explicit': track['explicit'],
            'played_at': item['played_at'],
        }

        rows.append(row)

    return pd.DataFrame(rows)


def create_df_artist_information():
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_artist_information.json")

    # Read data from the JSON file
    with open(raw_spotify_data_file, "r") as json_file:
        data = json.load(json_file)

    rows = []
    for artist in data['artists']:
        if len(artist['genres']) > 0:
            genre = simplify_genre(artist['genres'])
        else:
            genre = ""

        if genre == "":
            continue

        row = {
            'artist': artist['name'],
            'genre': genre,
        }

        rows.append(row)

    return pd.DataFrame(rows)


def create_df_track_features():
    raw_spotify_data_file = os.path.join(RAW_DATA_DIR, "spotify", "raw_spotify_track_features.json")

    # Read data from the JSON file
    with open(raw_spotify_data_file, "r") as json_file:
        data = json.load(json_file)

    rows = []
    for audio_feature in data['audio_features']:
        row = {
            'danceability': audio_feature['danceability'],
            'energy': audio_feature['energy'],
            'key': audio_feature['key'],
            'loudness': audio_feature['loudness'],
            'mode': audio_feature['mode'],
            'speechiness': audio_feature['speechiness'],
            'acousticness': audio_feature['acousticness'],
            'instrumentalness': audio_feature['instrumentalness'],
            'liveness': audio_feature['liveness'],
            'valence': audio_feature['valence'],
            'tempo': audio_feature['tempo'],
            'id': audio_feature['id'],
        }

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    df_recently_played = create_df_recently_played()
    df_track_features = create_df_track_features()
    df_artist_information = create_df_artist_information()

    df = pd.concat([df_recently_played, df_track_features], axis=1)
    df = pd.merge(df, df_artist_information, on='artist', how='inner')
    df = df.drop(columns=['id', 'artist'])

    column_rename_mapping = {
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
