from src.classes.data.DataManager import DataManager
from definitions import ROOT_DIR
import os
import joblib
import onnx
from mlflow import MlflowClient
import mlflow
import dagshub


class MlflowPlatform:
    def __init__(self):
        dagshub.auth.add_app_token(token=os.getenv("DAGSHUB_TOKEN"))
        dagshub.init(os.getenv("DAGSHUB_REPO_NAME"), os.getenv("DAGSHUB_USERNAME"), mlflow=True)
        mlflow.set_tracking_uri(os.getenv("DAGSHUB_URI"))
        self.client = MlflowClient()

    def save_pipeline(self, pipeline, pipeline_name, stage):
        pipeline = mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path=f"models/{pipeline_name}",
            registered_model_name=pipeline_name,
        )

        pipeline_version = self.client.create_model_version(
            name=pipeline_name,
            source=pipeline.model_uri,
            run_id=pipeline.run_id
        )

        self.client.transition_model_version_stage(
            name=pipeline_name,
            version=pipeline_version.version,
            stage=stage,
        )

    def save_model(self, model, model_name, stage):
        model = mlflow.onnx.log_model(
            onnx_model=model,
            artifact_path=f"models/{model_name}",
            registered_model_name=model_name,
        )

        model_version = self.client.create_model_version(
            name=model_name,
            source=model.model_uri,
            run_id=model.run_id
        )

        self.client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage=stage,
        )

    def download_onnx_model(self, model_name, stage):
        try:
            # Get model latest staging source
            latest_model_version_source = self.client.get_latest_versions(name=model_name, stages=[stage])[0].source

            # Load the model by its source
            return mlflow.onnx.load_model(latest_model_version_source)
        except IndexError:
            print(f"There was an error downloading {model_name} in {stage}")
            return None

    def download_pipeline(self, pipeline_name, stage):
        try:
            # Get pipeline latest staging source
            latest_pipeline_source = self.client.get_latest_versions(name=pipeline_name, stages=[stage])[0].source

            # Load the pipeline by its source
            return mlflow.sklearn.load_model(latest_pipeline_source)
        except IndexError:
            print(f"There was an error downloading {pipeline_name} in {stage}")
            return None

    def get_latest_model(self, stage):
        # Download model and pipeline for station
        model = self.download_onnx_model("classification_model", stage)
        pipeline = self.download_pipeline("classification_model_pipeline", stage)

        # Create model directory if it does not exist
        base_station_directory = os.path.join(ROOT_DIR, "models", "classification_model")
        DataManager.make_directory_if_missing(base_station_directory)

        # Save pipeline
        pipeline_path = os.path.join(base_station_directory, f"pipeline=classification_model.gz")
        joblib.dump(pipeline, pipeline_path)

        # Save model
        model_path = os.path.join(base_station_directory, f"model=classification_model.onnx")
        onnx.save_model(model, model_path)

        return model_path, pipeline