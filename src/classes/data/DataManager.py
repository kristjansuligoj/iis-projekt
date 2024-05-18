import pandas as pd
import json
import os


class DataManager:
    def __init__(self):
        print("heya")

    @staticmethod
    def save_to_csv(file_path, df, overwrite=False, notify=True):
        if not os.path.exists(file_path) or overwrite:
            df.to_csv(file_path, mode='w', index=False, header=True)
        else:
            df.to_csv(file_path, mode='a', index=False, header=False)

        if notify:
            print(f"Data saved to {file_path}")

    @staticmethod
    def save_to_json(file_path, data, overwrite=False, notify=True):
        if not os.path.exists(file_path) or overwrite:
            with open(file_path, "w") as json_file:
                json.dump(data, json_file)
        else:
            with open(file_path, "a") as json_file:
                json.dump(data, json_file)

        if notify:
            print(f"Data saved to {file_path}")

    @staticmethod
    def make_directory_if_missing(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    @staticmethod
    def clear_csv(df_file):
        # Clear the preprocessed files
        empty_df = pd.DataFrame()
        DataManager.save_to_csv(df_file, empty_df, overwrite=True, notify=False)
