from src.classes.spotify.spotify_token_manager import SpotifyTokenManager
from flask import Flask, jsonify, request, redirect
from dotenv import load_dotenv
from flask_cors import CORS

import os

load_dotenv()

spotify_authorization_url = os.getenv("SPOTIFY_AUTHORIZATION_URL")
spotify_api_token_url = os.getenv("SPOTIFY_API_TOKEN_URL")


def main():
    app = Flask(__name__)
    CORS(app)
    spotify_token_manager = SpotifyTokenManager()

    @app.route('/authorize', methods=['GET'])
    def authorize():
        # Read from .env file
        spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")

        url = (
            f"{spotify_authorization_url}?"
            f"response_type=code&"
            f"client_id={spotify_client_id}&"
            f"redirect_uri=http://localhost:8080&"
            f"scope=user-read-recently-played"
        )

        return redirect(url)

    @app.route('/', methods=['GET'])
    def save_access_token():
        query_params = request.args

        code = query_params.get('code')

        # If user is not authenticated yet,
        if code is None:
            api_url = os.getenv("CLIENT_SPOTIFY_AUTHORIZATION_URL")
            return redirect(f"{api_url}/authorize")

        spotify_token_manager.get_tokens(code)

        return jsonify("Authorization complete. You can close this site now.")

    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":
    main()
