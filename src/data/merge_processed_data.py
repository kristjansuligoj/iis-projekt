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

        # Clear the files for further use
        DataManager.clear_csv(df_spotify_file)
        DataManager.clear_csv(df_weather_file)

        df_spotify['date'] = pd.to_datetime(df_spotify['date'])
        df_weather['date'] = pd.to_datetime(df_weather['date'])

        # Merge weather data with previous response
        df_merged = pd.merge_asof(df_spotify, df_weather, on='date')

        df_merged_file = os.path.join(PROCESSED_DATA_DIR, "processed_data.csv")
        DataManager.save_to_csv(df_merged_file, df_merged)
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except IOError as e:
        print(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    main()
