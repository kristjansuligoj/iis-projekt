from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from definitions import PROCESSED_DATA_DIR
from sklearn.pipeline import Pipeline
from tensorflow import keras

import tensorflow_model_optimization as tmo
import tensorflow as tf
import pandas as pd
import onnxruntime
import numpy as np
import tf2onnx
import mlflow
import os


class ModelHelper:
    def __init__(self, ml_flow_platform):
        self.ml_flow_platform = ml_flow_platform

    def get_model_metrics(self, y_predictions, y_true):
        accuracy = accuracy_score(y_true, y_predictions)
        precision = precision_score(y_true, y_predictions, average='weighted')
        recall = recall_score(y_true, y_predictions, average='weighted')
        f1 = f1_score(y_true, y_predictions, average='weighted')

        return accuracy, precision, recall, f1

    def get_model_and_pipeline_from_stage(self, stage):
        print(f"\nRetrieving model from {stage}\n")
        model_path, pipeline = self.ml_flow_platform.get_latest_model(stage, "classification_model")

        if model_path is None or pipeline is None:
            print(f"Model or pipeline was not downloaded properly. Ending evaluation.")
            mlflow.end_run()
            return

        return onnxruntime.InferenceSession(model_path), pipeline

    def evaluate_model(self, model, X_test, y_test, stage):
        print(f"\nTraining latest {stage} model.\n")

        # Transform to float, because X_test is double otherwise
        X_test = X_test.astype(np.float32)

        # Get predictions
        model_predictions = model.run(["output"], {"input": X_test})[0]

        # Convert predicted probabilities to numeric labels
        y_pred_labels = np.argmax(model_predictions, axis=1)

        # Get metrics for latest model
        accuracy, precision, recall, f1 = self.get_model_metrics(y_pred_labels, y_test)

        if stage == "staging":
            # Log the metrics to Mlflow
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1", f1)

        return accuracy, precision, recall, f1

    def convert_model_to_onnx(self, model):
        # Otherwise conversion fails
        model.output_names = ["output"]

        input_signature = [
            tf.TensorSpec(shape=(None, 11), dtype=tf.float32, name="input")
        ]

        # Transform from keras to ONNX
        onnx_model, _ = tf2onnx.convert.from_keras(
            model=model,
            input_signature=input_signature,
            opset=13
        )

        return onnx_model

    def create_and_compile_model(self, input_shape, num_classes):
        model = keras.models.Sequential([
            keras.layers.Input(shape=input_shape),
            tmo.quantization.keras.quantize_annotate_layer(keras.layers.Dense(32, activation='relu')),
            keras.layers.Dropout(0.1),
            tmo.quantization.keras.quantize_annotate_layer(keras.layers.Dense(16, activation='relu')),
            keras.layers.Dropout(0.1),
            tmo.quantization.keras.quantize_annotate_layer(keras.layers.Dense(num_classes, activation='softmax')),
        ])

        tmo.quantization.keras.quantize_apply(model)

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        return model

    def separate_features_and_target(self, df, target_column):
        X = df.drop(columns=[target_column])
        y = df[target_column]
        return X, y

    # Function fills null values with the mean of the same genre
    def fill_na_with_genre_mean(self, df):
        # Identify columns to fill nulls (excluding 'genre')
        columns_to_fill = df.columns[df.isna().any()].tolist()

        for column in columns_to_fill:
            df[column] = df.groupby('genre')[column].transform(lambda x: x.fillna(x.mean()))

        return df

    def fill_null_values(self, df_train, df_test):
        # Drop rows where the 'genre' column is null
        df_train = df_train[df_train['genre'].notnull()]
        df_test = df_test[df_test['genre'].notnull()]

        # Fill null values in training and testing data
        df_train = self.fill_na_with_genre_mean(df_train)
        df_test = self.fill_na_with_genre_mean(df_test)

        return df_train, df_test

    def create_pipeline(self, ):
        # Define columns to transform
        columns_to_normalize = [
            'key', 'loudness', 'tempo', 'temperature', 'relative_humidity', 'dew_point', 'apparent_temperature',
            'precipitation_probability', 'surface_pressure'
        ]

        categorical_columns = ['explicit']

        # Define pipelines for preprocessing
        normalize_transformer = Pipeline([
            ('normalize', MinMaxScaler()),
        ])

        categorical_transformer = Pipeline([
            ('categorical', OneHotEncoder())
        ])

        # Define preprocessor
        preprocessor = ColumnTransformer([
            ('normalize_transformer', normalize_transformer, columns_to_normalize),
            ('categorical_transformer', categorical_transformer, categorical_columns),
        ])

        # Define pipeline
        return Pipeline([('preprocess', preprocessor)])

    def prepare_train_test_data(self, pipeline=None):
        df_train_path = os.path.join(PROCESSED_DATA_DIR, "train_data.csv")
        df_train = pd.read_csv(df_train_path)

        df_test_path = os.path.join(PROCESSED_DATA_DIR, "test_data.csv")
        df_test = pd.read_csv(df_test_path)

        # Fill the null values
        df_train, df_test = self.fill_null_values(df_train, df_test)

        # Separate features and target
        X_train, y_train = self.separate_features_and_target(df_train, 'genre')
        X_test, y_test = self.separate_features_and_target(df_test, 'genre')

        if pipeline is None:
            pipeline = self.create_pipeline()

        pipeline.fit(X_train, y_train)

        X_train = pipeline.transform(X_train)
        X_test = pipeline.transform(X_test)

        # One-hot encode the target feature (genre)
        label_encoder = LabelEncoder()
        y_train = label_encoder.fit_transform(y_train)
        y_test = label_encoder.transform(y_test)

        return X_train, y_train, X_test, y_test, pipeline
