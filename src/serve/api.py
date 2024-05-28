from src.classes.spotify.spotify_token_manager import SpotifyTokenManager
from flask import Flask, jsonify, request, make_response, send_file
from src.classes.data.DatabaseManager import DatabaseManager
from src.classes.spotify.spotify_client import SpotifyClient
from src.classes.mlflow.mlflow_platform import MlflowPlatform
from geventwebsocket.handler import WebSocketHandler
from flask_socketio import SocketIO
from definitions import ROOT_DIR
from dotenv import load_dotenv
from flask_cors import CORS
from gevent import pywsgi

import api_helpers
import threading
import os

load_dotenv()

spotify_authorization_url = os.getenv("SPOTIFY_AUTHORIZATION_URL")
spotify_api_token_url = os.getenv("SPOTIFY_API_TOKEN_URL")

spotify_token_manager = SpotifyTokenManager()
spotify_client = SpotifyClient()
database_manager = DatabaseManager()
ml_flow_platform = MlflowPlatform()


def api():
    app = Flask(__name__)
    CORS(app)

    classification_model, classification_pipeline = api_helpers.get_model_and_pipeline_from_stage("production")
    musicgen_pipeline = ml_flow_platform.get_musicgen_pipeline()

    def generate_track_async(df_input, genre):
        print("Track is being generated")

        # Generate track
        track = api_helpers.generate_track(musicgen_pipeline, df_input, genre)

        print("Track generated.")

        # Save track to file
        track_file_name = api_helpers.save_track_to_file(track, genre)

    @app.route('/api/tracks/download-specific', methods=['GET'])
    def download_track():
        track_file_name = request.args.get('track_file_name')

        if track_file_name is None:
            return jsonify("Track file name missing.", 400)

        track_path = os.path.join(ROOT_DIR, "tracks", track_file_name)

        return send_file(track_path, as_attachment=True)

    @app.route('/api/tracks/recently-played', methods=['GET'])
    def get_recently_played_tracks():
        tracks = spotify_client.get_recently_played_tracks()
        return make_response(jsonify(tracks), 200)

    @app.route('/api/tracks/list', methods=['GET'])
    def list_tracks():
        # Directory where your tracks are stored
        tracks_dir = os.path.join(ROOT_DIR, "tracks")

        # List all files in the tracks directory
        track_files = os.listdir(tracks_dir)

        # Assuming you want to return just the filenames
        track_filenames = [filename for filename in track_files if os.path.isfile(os.path.join(tracks_dir, filename))]

        return jsonify(track_filenames, 200)

    @app.route('/api/tracks/generate', methods=['POST'])
    def generate_music():
        print("Predicting genre . . .")

        track_data = request.get_json()

        # Check if data is received
        if not track_data:
            return jsonify({"error": "No data provided"}), 400

        # Create model input
        X_predict, df_input = api_helpers.create_model_input(classification_pipeline, track_data)

        # Predict the genre
        genre = api_helpers.predict_genre(classification_model, X_predict)

        # Insert prediction to database
        api_helpers.add_prediction_to_database(df_input, genre)

        # Start creating a track on a separate track
        threading.Thread(target=generate_track_async, args=(df_input, genre)).start()

        return jsonify('Your track is being generated. This could take some time.', 200)

    @app.route('/api/authorize', methods=['GET'])
    def save_access_token():
        query_params = request.args

        code = query_params.get('code')

        # If user is not authenticated yet
        if code is None:
            return make_response(jsonify("Code is missing. Authenticate with Spotify first."), 401)

        spotify_token_manager.get_tokens(code)
        return make_response(jsonify("Authorization complete. You can close this site now."), 200)

    @app.route('/api/authorize/check', methods=['GET'])
    def check_if_authorized():
        _, refresh_token = database_manager.fetch_latest_tokens()

        if refresh_token == "":
            return make_response(jsonify("You are not authorized."), 401)

        return make_response(jsonify("You are authorized."), 200)

    @app.route('/api/metrics/production-accuracy', methods=['GET'])
    def get_production_metrics():
        production_metrics = database_manager.fetch_data('production_accuracy', sort_field='datetime')
        return make_response(jsonify(production_metrics), 200)

    @app.route('/api/metrics/metrics-of-today', methods=['GET'])
    def get_metrics_of_today():
        metrics_of_today = ml_flow_platform.get_last_run_from_experiment('Past predictions')
        return make_response(jsonify(metrics_of_today), 200)

    print("Starting server. . .")
    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":
    api()
