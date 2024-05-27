from definitions import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.classes.data.DataManager import DataManager

import pandas as pd
import os


# If a song is listened to at 11 am, the next time the GitHub Actions is ran could be the next day, so weather data
# is missing, and validation fails, until you manually fix the data. This prevents that with checking all weather data
# in the past and maps the missing data
def check_if_weather_data_exists(df):
    weather_columns = [
        'temperature', 'relative_humidity', 'dew_point', 'apparent_temperature', 'precipitation_probability', 'rain',
        'surface_pressure'
    ]

    # Get the indices of rows with missing values in any of the specified columns
    missing_indices = df[weather_columns].isna().any(axis=1).to_numpy().nonzero()[0]

    print(missing_indices)

    print(df.to_string(index=False))

    # Check if any of the specified columns contain NaN values
    if len(missing_indices) > 0:
        # We need all weather data, so we can fill the missing values
        all_file_path = os.path.join(RAW_DATA_DIR, 'weather', 'all_weather.csv')
        df_all_weather = pd.read_csv(all_file_path)

        # Convert 'date' columns to datetime in both DataFrames for proper merging
        df['date'] = pd.to_datetime(df['date'])
        df_all_weather['date'] = pd.to_datetime(df_all_weather['date'])

        # Fill missing values in specified columns with data from df_all_weather
        for index in missing_indices:
            # Find the row that is the closest to the track date (Weather is 1:00:00, track can be 1:23:03)
            date = df.loc[index, 'date']
            nearest_row = df_all_weather.iloc[(df_all_weather['date'] - date).abs().argsort()[0]]

            # Fill the values from the nearest row
            for columns in weather_columns:
                df.loc[index, columns] = nearest_row[columns]

    return df


def main():
    try:
        df_spotify_file = os.path.join(RAW_DATA_DIR, "spotify", "preprocessed_spotify_data.csv")
        df_spotify = pd.read_csv(df_spotify_file)

        df_weather_file = os.path.join(RAW_DATA_DIR, "weather", "preprocessed_weather_data.csv")
        df_weather = pd.read_csv(df_weather_file)

        df_processed_data = os.path.join(PROCESSED_DATA_DIR, "processed_data.csv")
        df = pd.read_csv(df_processed_data)

        # Clear the files for further use
        # DataManager.clear_csv(df_spotify_file)
        # DataManager.clear_csv(df_weather_file)

        df_spotify['date'] = pd.to_datetime(df_spotify['date'])
        df_weather['date'] = pd.to_datetime(df_weather['date'])
        df['date'] = pd.to_datetime(df['date'])

        # Merge weather data with previous response
        df_merged = pd.merge_asof(df_spotify, df_weather, on='date')

        # Desired column order
        desired_order = [
            'date', 'genre', 'explicit', 'danceability', 'energy', 'key',
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
        df.reset_index(drop=True, inplace=True)

        # Sort by date to keep them in order
        df = df.sort_values(by='date')

        # Check if any row has missing weather data, and fill it if it does
        df = check_if_weather_data_exists(df)

        df_merged_file = os.path.join(PROCESSED_DATA_DIR, "processed_data.csv")
        DataManager.save_to_csv(df_merged_file, df, overwrite=True)
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except IOError as e:
        print(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    main()
