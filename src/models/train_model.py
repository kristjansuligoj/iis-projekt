from src.classes.mlflow.mlflow_platform import MlflowPlatform
from src.models.model_helpers import ModelHelper
from dotenv import load_dotenv
import numpy as np

import mlflow

load_dotenv()


def train_model():
    ml_flow_platform = MlflowPlatform()
    model_helper = ModelHelper(ml_flow_platform)
    epochs = 5
    batch_size = 5
    validation_split = 0.2

    # # Start the Mlflow run
    mlflow.start_run(run_name=f"classification_model", experiment_id="2")

    # Prepare train and test data
    X_train, y_train, X_test, y_test, pipeline = model_helper.prepare_train_test_data()

    # Get the input shape for the model
    input_shape = (X_train.shape[1],)
    num_classes = len(np.unique(y_train))

    # Build and compile the model
    model = model_helper.create_and_compile_model(input_shape=input_shape, num_classes=num_classes)

    # Train the model
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split)

    mlflow.log_param("epochs", epochs)
    mlflow.log_param("batch_size", batch_size)
    mlflow.log_param("validation_split", validation_split)
    mlflow.log_param("train_dataset_size", len(X_train) + len(y_train))

    # Convert model to Onnx model
    onnx_model = model_helper.convert_model_to_onnx(model)

    # Save model and pipeline to Mlflow
    ml_flow_platform.save_model(onnx_model, "classification_model", "staging")
    ml_flow_platform.save_pipeline(pipeline, "classification_model_pipeline", "staging")

    # End the Mlflow run
    mlflow.end_run()


if __name__ == "__main__":
    train_model()

