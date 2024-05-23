from src.models.model_helpers import prepare_train_test_data, create_and_compile_model, convert_model_to_onnx
from src.classes.mlflow.mlflow_platform import MlflowPlatform
from dotenv import load_dotenv

import mlflow

load_dotenv()


def train_model():
    ml_flow_platform = MlflowPlatform()

    # Start the Mlflow run
    mlflow.start_run(run_name=f"run=train_model")
    mlflow.tensorflow.autolog()

    # Prepare train and test data
    X_train, y_train, X_test, y_test, pipeline = prepare_train_test_data()

    # Get the input shape for the model
    input_shape = (X_train.shape[1],)

    # Build and compile the model
    model = create_and_compile_model(input_shape=input_shape)

    # Train the model
    model.fit(X_train, y_train, epochs=20, batch_size=5, validation_split=0.2)

    # Convert model to Onnx model
    onnx_model = convert_model_to_onnx(model)

    # Save model and pipeline to Mlflow
    ml_flow_platform.save_model(onnx_model, "classification_model", "production")
    ml_flow_platform.save_pipeline(pipeline, "classification_model_pipeline", "production")

    # End the Mlflow run
    mlflow.end_run()


if __name__ == "__main__":
    train_model()

