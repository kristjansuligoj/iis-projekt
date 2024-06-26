from src.classes.requests.requests_client import RequestsClient
from src.classes.data.DatabaseManager import DatabaseManager
import base64
import os


class SpotifyTokenManager:
    def __init__(self):
        self.database_manager = DatabaseManager()
        self.requests_client = RequestsClient()

        self.spotify_api_token_url = os.getenv("SPOTIFY_API_TOKEN_URL")
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self.access_token, self.refresh_token = self.database_manager.fetch_latest_tokens()

        client_credentials = f'{self.client_id}:{self.client_secret}'
        self.client_credentials_base64 = base64.b64encode(client_credentials.encode()).decode()

    # Uses the Authorization Code, to generate access and refresh tokens, then saves them to the database
    # https://developer.spotify.com/documentation/web-api/tutorials/code-flow
    def get_tokens(self, code):
        response = self.requests_client.send_request(
            method="POST",
            url=self.spotify_api_token_url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {self.client_credentials_base64}'
            },
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri
            }
        )

        access_token = response['access_token']
        refresh_token = response['refresh_token']

        self.access_token = access_token
        self.refresh_token = refresh_token

        # Insert both tokens to the database
        self.database_manager.insert_token('tokens', 'access', access_token)
        self.database_manager.insert_token('tokens', 'refresh', refresh_token)
        pass

    # Uses a refresh token to generate a new access token
    def get_new_access_token_with_refresh_token(self):
        response = self.requests_client.send_request(
            method="POST",
            url=self.spotify_api_token_url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {self.client_credentials_base64}'
            },
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
            }
        )

        access_token = response['access_token']

        self.access_token = access_token

        # Insert new access token to the database
        self.database_manager.insert_token('tokens', 'access', access_token)
        pass
