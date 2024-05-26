from src.classes.data.DataManager import DataManager
from definitions import RAW_DATA_DIR

import pandas as pd
from datetime import datetime
import os


def main():
    try:
        # Read all weather data
        all_file_path = os.path.join(RAW_DATA_DIR, 'weather', 'all_weather.csv')
        all_df = pd.read_csv(all_file_path)
        all_df['date'] = pd.to_datetime(all_df['date'])

        # Read today's weather
        today_weather_file = os.path.join(RAW_DATA_DIR, 'weather', 'raw_weather.csv')
        df_today = pd.read_csv(today_weather_file)

        today_date = datetime.now().date()

        # If today weather data does not yet exist, save it
        if not (today_date in all_df['date'].dt.date.unique()):
            all_df_file = os.path.join(RAW_DATA_DIR, 'weather', 'all_weather.csv')
            DataManager.save_to_csv(all_df_file, df_today)

        # Save to preprocessed file
        preprocessed_file_path = os.path.join(RAW_DATA_DIR, 'weather', 'preprocessed_weather_data.csv')
        DataManager.save_to_csv(preprocessed_file_path, df_today, overwrite=True)
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except IOError as e:
        print(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    main()
