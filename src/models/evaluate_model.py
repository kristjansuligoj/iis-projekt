from src.classes.mlflow.mlflow_platform import MlflowPlatform
from src.classes.data.DatabaseManager import DatabaseManager
from src.classes.data.DataManager import DataManager
from src.models.model_helpers import ModelHelper
from definitions import ROOT_DIR
from dotenv import load_dotenv
from datetime import datetime

import mlflow
import os

load_dotenv()


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


def evaluate_models():
    ml_flow_platform = MlflowPlatform()
    model_helper = ModelHelper(ml_flow_platform)
    database_manager = DatabaseManager()

    mlflow.start_run(run_name=f"classification_model", experiment_id="2")

    # Get latest model from staging and production
    staging_model, staging_pipeline = model_helper.get_model_and_pipeline_from_stage("staging")
    production_model, production_pipeline = model_helper.get_model_and_pipeline_from_stage("production")

    print(f"\nCreating train and test data.\n")

    X_train, y_train, X_test, y_test, _ = model_helper.prepare_train_test_data(staging_pipeline)

    mlflow.log_param("train_dataset_size", len(X_train) + len(y_train))

    # Evaluate models
    staging_accuracy, staging_precision, staging_recall, staging_f1 = model_helper.evaluate_model(
        staging_model, X_test, y_test, "staging"
    )

    production_accuracy, _, _, _ = model_helper.evaluate_model(
        production_model, X_test, y_test, "production"
    )

    model_name = "classification_model"

    # Check if new model is better than production, and replace it if it is
    if staging_accuracy > production_accuracy:
        print("New model was better than the one in production. Replacing it now . . .")
        ml_flow_platform.replace_prod_model(model_name)

        production_accuracy = {
            'datetime': datetime.now(),
            'accuracy': staging_accuracy,
        }

        database_manager.insert_data("production_accuracy", production_accuracy)

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
