from definitions import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.classes.data.DataManager import DataManager

import pandas as pd
import os


def main():
    try:
        df_spotify_file = os.path.join(RAW_DATA_DIR, "spotify", "preprocessed_spotify_data.csv")
        df_spotify = pd.read_csv(df_spotify_file)

        df_weather_file = os.path.join(RAW_DATA_DIR, "weather", "preprocessed_weather_data.csv")
        df_weather = pd.read_csv(df_weather_file)

        df_processed_data = os.path.join(PROCESSED_DATA_DIR, "processed_data.csv")
        df = pd.read_csv(df_processed_data)

        # Clear the files for further use
        DataManager.clear_csv(df_spotify_file)
        DataManager.clear_csv(df_weather_file)

        df_spotify['date'] = pd.to_datetime(df_spotify['date'])
        df_weather['date'] = pd.to_datetime(df_weather['date'])
        df['date'] = pd.to_datetime(df['date'])

        # Merge weather data with previous response
        df_merged = pd.merge_asof(df_spotify, df_weather, on='date')

        # Desired column order
        desired_order = [
            'date', 'artists', 'name', 'length', 'explicit', 'popularity', 'danceability', 'energy', 'key',
            'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence',
            'tempo', 'temperature', 'relative_humidity', 'dew_point', 'apparent_temperature',
            'precipitation_probability', 'rain', 'surface_pressure'
        ]

        # Reorder the columns
        df_merged = df_merged[desired_order]

        # Add the newly fetched data
        df = pd.concat([df, df_merged])

        # Drop if any track is repeated. This can happen if user has not listened to any new songs since last fetch
        df = df.drop_duplicates(subset=['date'])

        # Sort by date to keep them in order
        df = df.sort_values(by='date')

        df_merged_file = os.path.join(PROCESSED_DATA_DIR, "processed_data.csv")
        DataManager.save_to_csv(df_merged_file, df, overwrite=True)
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except IOError as e:
        print(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    main()
