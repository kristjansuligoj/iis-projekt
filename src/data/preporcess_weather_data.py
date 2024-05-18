from src.classes.data.DataManager import DataManager
from definitions import RAW_DATA_DIR

import pandas as pd
import os


def main():
    try:
        # Read today's weather
        today_weather_file = os.path.join(RAW_DATA_DIR, 'weather', 'raw_weather.csv')
        df_today = pd.read_csv(today_weather_file)

        # Some processing . . .

        # Save to preprocessed file
        preprocessed_file_path = os.path.join(RAW_DATA_DIR, 'weather', 'preprocessed_weather_data.csv')
        DataManager.save_to_csv(preprocessed_file_path, df_today, overwrite=True)
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")
    except IOError as e:
        print(f"An error occurred while processing the file: {e}")


if __name__ == "__main__":
    main()
