from definitions import PROCESSED_DATA_DIR
import pandas as pd
import os


def main():
    df_file = os.path.join(PROCESSED_DATA_DIR, "processed_data.csv")
    df = pd.read_csv(df_file)

    # Sort data by date
    station_data = df.sort_values(by="date", ascending=False)

    # Get test size
    test_size = int(len(station_data) * 0.1)

    # Split to train/test data
    train_data = station_data.iloc[test_size:]
    test_data = station_data.iloc[:test_size]

    # Save train/test data
    train_data.to_csv(os.path.join(PROCESSED_DATA_DIR, f"train_data.csv"), index=False)
    test_data.to_csv(os.path.join(PROCESSED_DATA_DIR, f"test_data.csv"), index=False)


if __name__ == "__main__":
    main()
