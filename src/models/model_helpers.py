from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder
import tensorflow as tf
from tensorflow import keras
from sklearn.compose import ColumnTransformer
from definitions import PROCESSED_DATA_DIR
from sklearn.pipeline import Pipeline


import tensorflow_model_optimization as tmo
import pandas as pd
import tf2onnx
import os


def convert_model_to_onnx(model):
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


def create_and_compile_model(input_shape, num_classes):
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


def separate_features_and_target(df, target_column):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y


# Function fills null values with the mean of the same genre
def fill_na_with_genre_mean(df):
    # Identify columns to fill nulls (excluding 'genre')
    columns_to_fill = df.columns[df.isna().any()].tolist()

    for column in columns_to_fill:
        df[column] = df.groupby('genre')[column].transform(lambda x: x.fillna(x.mean()))

    return df


def fill_null_values(df_train, df_test):
    # Drop rows where the 'genre' column is null
    df_train = df_train[df_train['genre'].notnull()]
    df_test = df_test[df_test['genre'].notnull()]

    # Fill null values in training and testing data
    df_train = fill_na_with_genre_mean(df_train)
    df_test = fill_na_with_genre_mean(df_test)

    return df_train, df_test


def create_pipeline():
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


def prepare_train_test_data(pipeline=None):
    df_train_path = os.path.join(PROCESSED_DATA_DIR, "train_data.csv")
    df_train = pd.read_csv(df_train_path)

    df_test_path = os.path.join(PROCESSED_DATA_DIR, "test_data.csv")
    df_test = pd.read_csv(df_test_path)

    # Fill the null values
    df_train, df_test = fill_null_values(df_train, df_test)

    # Separate features and target
    X_train, y_train = separate_features_and_target(df_train, 'genre')
    X_test, y_test = separate_features_and_target(df_test, 'genre')

    if pipeline is None:
        pipeline = create_pipeline()

    pipeline.fit(X_train, y_train)

    X_train = pipeline.transform(X_train)
    X_test = pipeline.transform(X_test)

    # One-hot encode the target feature (genre)
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.transform(y_test)

    return X_train, y_train, X_test, y_test, pipeline
