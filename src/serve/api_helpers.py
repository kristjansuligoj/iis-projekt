from src.classes.mlflow.mlflow_platform import MlflowPlatform
from src.classes.data.DatabaseManager import DatabaseManager
from definitions import ROOT_DIR, RAW_DATA_DIR
from mlflow.exceptions import RestException
from transformers import pipeline
from datetime import datetime

import scipy.io.wavfile
import pandas as pd
import onnxruntime
import numpy as np
import torch
import time
import os

ml_flow_platform = MlflowPlatform()
database_manager = DatabaseManager()


def get_prompt(df_input, genre):
    # Initialize the base of the prompt
    prompt = f"{genre} song that is "

    # Define conditions for each attribute
    conditions = {
        "acousticness": ["not acoustic", "somewhat acoustic", "very acoustic"],
        "danceability": ["not danceable", "danceable", "very danceable"],
        "energy": ["not energetic", "energetic", "very energetic"],
        "instrumentalness": ["not instrumental", "somewhat instrumental", "very instrumental"],
        "liveness": ["not lively", "lively", "very lively"],
        "loudness": ["very quiet", "quiet", "loud"],
        "mode": ["in a minor key", "in a major key"],
        "speechiness": ["not speechy", "somewhat speechy", "very speechy"],
        "valence": ["not happy", "somewhat happy", "very happy"],
        "explicit": ["not explicit", "explicit"]
    }

    # Check each attribute and append the corresponding condition to the prompt
    for attribute, labels in conditions.items():
        value = df_input[attribute][0]

        print(f"attribute: {attribute}, value: {value}")

        if attribute == "explicit":
            prompt += f"{labels[int(value)]}, "
        elif attribute == "mode":
            prompt += f"{labels[int(value)]}, "
        elif attribute == "loudness":
            if value < -40:
                prompt += f"{labels[0]}, "
            elif value < -20:
                prompt += f"{labels[1]}, "
            else:
                prompt += f"{labels[2]}, "
        else:
            if value < 0.33:
                prompt += f"{labels[0]}, "
            elif value < 0.66:
                prompt += f"{labels[1]}, "
            else:
                prompt += f"{labels[2]}, "

    # Add the tempo and key
    prompt += f"around {df_input['tempo'][0]} BPM, "
    prompt += f"in key {df_input['key'][0]}."

    # Remove trailing comma and space
    prompt = prompt.rstrip(", ")

    return prompt


def map_prediction_with_genre(index):
    genre_mappings = ['classical', 'hip hop', 'pop', 'rap', 'metal', 'country', 'lo-fi', 'indie', 'rock']
    return genre_mappings[index]


def get_model_and_pipeline_from_stage(stage):
    print(f"\nRetrieving model from {stage}\n")
    model_path, model_pipeline = ml_flow_platform.get_latest_model(stage, "classification_model")

    return onnxruntime.InferenceSession(model_path), model_pipeline


def is_model_already_downloaded(model_path, pipeline_path):
    return os.path.exists(model_path) and os.path.exists(pipeline_path)


def download_model(name):
    print("Checking if models exist locally, and download them otherwise.")

    model_path = os.path.join(ROOT_DIR, "models", name, f"model={name}.onnx")
    pipeline_path = os.path.join(ROOT_DIR, "models", name, f"pipeline={name}.gz")

    # Check if model is already downloaded, and skip this station if it is
    if is_model_already_downloaded(model_path, pipeline_path):
        print(f"Model {name} already loaded. Skipping. . .")
        return

    try:
        ml_flow_platform.get_latest_model("production", name)
    except RestException:
        print(f"There was an error downloading {name}")
        return


def download_musicgen_model():
    # Check if a GPU is available and use it
    device = 0 if torch.cuda.is_available() else -1

    return pipeline("text-to-audio", model="facebook/musicgen-small", device=device)


def get_weather_data():
    # Read weather data from today
    df_weather_path = os.path.join(RAW_DATA_DIR, "weather", "raw_weather.csv")
    df_weather = pd.read_csv(df_weather_path)

    # Convert 'date' column to datetime
    df_weather['date'] = pd.to_datetime(df_weather['date'])

    # Get current hour
    current_hour = datetime.now().hour

    # Find the row that is closest to the current hour
    return df_weather.iloc[(df_weather['date'].dt.hour - current_hour).abs().argsort()[0]]


def save_track_to_file(track, genre):
    print(f"Track generated. Saving it to file now.")

    current_timestamp = int(time.time())
    wav_file_path = os.path.join(ROOT_DIR, "tracks", f"{current_timestamp}-{genre}-track.wav")

    # Save the generated audio
    scipy.io.wavfile.write(wav_file_path, rate=track["sampling_rate"], data=track["audio"])

    print(f"Track saved to {wav_file_path}")

    return f"{current_timestamp}.wav"


def predict_genre(classification_model, X_predict):
    # Transform to float, because X_test is double otherwise
    X_predict = X_predict.astype(np.float32)

    model_prediction = classification_model.run(
        ["output"],
        {"input": X_predict}
    )[0]

    # Convert predicted probabilities to numeric labels
    y_pred_labels = np.argmax(model_prediction, axis=1)[0]

    genre = map_prediction_with_genre(y_pred_labels)

    print(f"Predicted genre is {genre}")

    return genre


def generate_track(musicgen_model, df_input, genre):
    # Track length in seconds
    duration = 5

    # Steps per second the model uses
    steps_per_second = 50

    # Max length
    max_length = duration * steps_per_second

    prompt = get_prompt(df_input, genre)

    print(f"Generating track with prompt: {prompt}")

    # Generate track with optimized parameters
    return musicgen_model(
        prompt, forward_params={
            "do_sample": True,
            "num_beams": 1,
            "max_length": max_length,
        }
    )


def create_model_input(classification_pipeline, track_data):
    weather_data = get_weather_data()

    df_track = pd.DataFrame([track_data])
    df_weather = pd.DataFrame([weather_data])

    # Reset the index to avoid duplicate indices during concatenation
    df_track = df_track.reset_index(drop=True)
    df_weather = df_weather.reset_index(drop=True)

    df_input = pd.concat([df_track, df_weather], axis=1)

    return classification_pipeline.transform(df_input), df_input


def add_prediction_to_database(df_input, genre):
    track_data_dict = df_input.to_dict(orient='records')

    prediction = {
        'prediction': genre,
        'datetime': datetime.now(),
        'track_data': track_data_dict,
    }

    database_manager.insert_data("predictions", prediction)
