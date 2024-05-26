from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.classes.mlflow.mlflow_platform import MlflowPlatform
from src.models.model_helpers import prepare_train_test_data
from src.classes.data.DataManager import DataManager
from definitions import ROOT_DIR
from dotenv import load_dotenv

import mlflow
import onnxruntime
import numpy as np
import os

load_dotenv()
ml_flow_platform = MlflowPlatform()

genres = {
    'classical': 'classical',
    'hip hop': 'hip hop',
    'pop': 'pop',
    'rap': 'rap',
    'metal': 'metal',
    'country': 'country',
    'lo-fi': 'lo-fi',
    'indie': 'indie',
    'rock': 'rock',
}


def get_model_metrics(y_predictions, y_true):
    accuracy = accuracy_score(y_true, y_predictions)
    precision = precision_score(y_true, y_predictions, average='weighted')
    recall = recall_score(y_true, y_predictions, average='weighted')
    f1 = f1_score(y_true, y_predictions, average='weighted')

    return accuracy, precision, recall, f1


def get_model_and_pipeline_from_stage(stage):
    print(f"\nRetrieving model from {stage}\n")
    model_path, pipeline = ml_flow_platform.get_latest_model(stage, "classification_model")

    if model_path is None or pipeline is None:
        print(f"Model or pipeline was not downloaded properly. Ending evaluation.")
        mlflow.end_run()
        return

    return onnxruntime.InferenceSession(model_path), pipeline


def evaluate_model(model, X_test, y_test, stage):
    print(f"\nTraining latest {stage} model.\n")

    # Transform to float, because X_test is double otherwise
    X_test = X_test.astype(np.float32)

    # Get predictions
    model_predictions = model.run(["output"], {"input": X_test})[0]

    # Convert predicted probabilities to numeric labels
    y_pred_labels = np.argmax(model_predictions, axis=1)

    # Get metrics for latest model
    accuracy, precision, recall, f1 = get_model_metrics(y_pred_labels, y_test)

    if stage == "staging":
        # Log the metrics to Mlflow
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)

    return accuracy, precision, recall, f1


def evaluate_models():
    mlflow.start_run(run_name=f"run=evaluate_model")
    mlflow.tensorflow.autolog()

    # Get latest model from staging and production
    staging_model, staging_pipeline = get_model_and_pipeline_from_stage("staging")
    production_model, production_pipeline = get_model_and_pipeline_from_stage("production")

    print(f"\nCreating train and test data.\n")

    X_train, y_train, X_test, y_test, _ = prepare_train_test_data(staging_pipeline)

    mlflow.log_param("train_dataset_size", len(X_train) + len(y_train))

    # Evaluate models
    staging_accuracy, staging_precision, staging_recall, staging_f1 = evaluate_model(
        staging_model, X_test, y_test, "staging"
    )

    production_accuracy, _, _, _ = evaluate_model(
        production_model, X_test, y_test, "production"
    )

    model_name = "classification_model"

    # Check if new model is better than production, and replace it if it is
    if staging_accuracy > production_accuracy:
        print("New model was better than the one in production. Replacing it now . . .")
        ml_flow_platform.replace_prod_model(model_name)

    # Save metrics to file
    print(f"\nSaving metrics to file for model '{model_name}'\n")

    DataManager.make_directory_if_missing(os.path.join(ROOT_DIR, "reports"))
    with open(ROOT_DIR + f'/reports/model={model_name}_metrics.txt', 'w', encoding='utf-8') as f:
        f.write(
            f'Accuracy: {staging_accuracy}\n'
            f'Precision score: {staging_precision}\n'
            f'Recall score: {staging_recall}\n'
            f'F1 score: {staging_f1}\n'
        )

    mlflow.end_run()


if __name__ == "__main__":
    evaluate_models()
