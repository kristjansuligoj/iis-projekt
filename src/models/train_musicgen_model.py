from src.classes.mlflow.mlflow_platform import MlflowPlatform
from src.models.model_helpers import ModelHelper
from dotenv import load_dotenv
from src.serve.api_helpers import download_musicgen_model
import numpy as np
import torch
from transformers import pipeline
import mlflow

load_dotenv()


def train_model():
    ml_flow_platform = MlflowPlatform()
    model_helper = ModelHelper(ml_flow_platform)

    # # Start the Mlflow run
    mlflow.start_run(run_name=f"musicgen_pipeline", experiment_id="2")

    # Get latest model from staging and production
    musicgen_pipeline = download_musicgen_model()

    # Save model and pipeline to Mlflow
    ml_flow_platform.save_pipeline(musicgen_pipeline, "musicgen_pipeline", "production")

    # End the Mlflow run
    mlflow.end_run()


if __name__ == "__main__":
    train_model()


