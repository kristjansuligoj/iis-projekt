from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.classes.mlflow.mlflow_platform import MlflowPlatform
from src.classes.data.DatabaseManager import DatabaseManager
from definitions import PROCESSED_DATA_DIR
from scipy.spatial.distance import cdist
from dotenv import load_dotenv

import pandas as pd
import numpy as np
import mlflow
import os

load_dotenv()


# Function to normalize numeric columns for similarity comparison
def normalize(df):
    return (df - df.min()) / (df.max() - df.min())


def get_predictions_from_today():
    database_manager = DatabaseManager()

    # Get all predictions from the database for this station and day
    predictions_of_today = database_manager.fetch_predictions_from_today()

    if not predictions_of_today:
        return

    # Extract track_data from predictions_of_today
    track_data_list = []
    for prediction in predictions_of_today:
        if 'track_data' in prediction:
            track_data = prediction['track_data']
            for track in track_data:
                track['_id'] = prediction['_id']
                track['prediction'] = prediction['prediction']
                track['datetime'] = prediction['datetime']
                track_data_list.append(track)

    # Convert the list of track data into a DataFrame
    return pd.DataFrame(track_data_list)


def find_most_similar_rows(df_true, df_predictions):
    numeric_columns = [
        'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness',
        'mode', 'speechiness', 'tempo', 'valence', 'temperature', 'relative_humidity',
        'dew_point', 'apparent_temperature', 'precipitation_probability', 'rain', 'surface_pressure'
    ]

    # Normalize the DataFrames
    df_predictions_norm = normalize(df_predictions[numeric_columns])
    df_true_norm = normalize(df_true[numeric_columns])

    # Compute the distance matrix between the rows of the normalized DataFrames
    distances = cdist(df_predictions_norm, df_true_norm, metric='euclidean')

    # Find the index of the most similar row in df_true for each row in df_predictions
    closest_indices = np.argmin(distances, axis=1)

    # Retrieve the most similar rows from df_true
    return df_true.iloc[closest_indices]


def main():
    ml_flow_platform = MlflowPlatform()

    mlflow.start_run(run_name=f"experiment=evaluate_past_predictions", experiment_id="3")

    # Get predictions from today
    df_predictions = get_predictions_from_today()

    if df_predictions is None:
        mlflow.log_metric("total_predictions", 0)
        mlflow.end_run()
        return

    # Get actual values
    df_true_path = os.path.join(PROCESSED_DATA_DIR, "processed_data.csv")
    df_true = pd.read_csv(df_true_path)

    # Find the most similar rows
    most_similar_rows = find_most_similar_rows(df_true, df_predictions)

    # Add the actual genre from the most similar rows to df_predictions
    df_predictions['true'] = most_similar_rows['genre'].values

    # Get predictions and true values
    y_true = df_predictions['true'].tolist()
    y_pred = df_predictions['prediction'].tolist()

    # Calculate the average error of model
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')

    # Calculate the count of predictions and false predictions
    total_predictions = len(df_predictions)
    false_predictions = sum(1 for true, pred in zip(y_true, y_pred) if true != pred)

    # Log the metrics to Mlflow
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1", f1)
    mlflow.log_metric("total_predictions", total_predictions)
    mlflow.log_metric("false_predictions", false_predictions)

    mlflow.end_run()


if __name__ == "__main__":
    main()
