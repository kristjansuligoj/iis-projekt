from src.classes.spotify.spotify_token_manager import SpotifyTokenManager
from src.classes.requests.requests_client import RequestsClient
import os
import base64


class SpotifyClient:
    def __init__(self):
        self.spotify_authorization_url = os.getenv("SPOTIFY_AUTHORIZATION_URL")
        self.spotify_api_token_url = os.getenv("SPOTIFY_API_TOKEN_URL")
        self.spotify_api_url = os.getenv("SPOTIFY_API_URL")
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        client_credentials = f'{self.client_id}:{self.client_secret}'
        self.client_credentials_base64 = base64.b64encode(client_credentials.encode()).decode()

        self.token_manager = SpotifyTokenManager()
        self.requests_client = RequestsClient()

    # Sends an authenticated request to the spotify API.
    # The request is attempted using an access token, and if it is expired,
    # it uses a refresh token, to get a new access token.
    def send_authenticated_request(self, method, url, data=None):
        response = self.requests_client.send_request(
            method=method,
            url=url,
            headers={
                'Authorization': f'Bearer {self.token_manager.access_token}'
            },
            data=data
        )

        if 'error' in response:
            print("Attempting to refresh access token and retrying the request")
            self.token_manager.get_new_access_token_with_refresh_token()

            # Retry the request with the new access token
            response = self.requests_client.send_request(
                method=method,
                url=url,
                headers={
                    'Authorization': f'Bearer {self.token_manager.access_token}'
                },
                data=data
            )

        return response

    # Get recently played tracks of the authenticated user
    def get_recently_played_tracks(self, limit=50):
        return self.send_authenticated_request(
            method="GET",
            url=f"{self.spotify_api_url}/me/player/recently-played?limit={limit}",
        )

    # Get audio features of the provided tracks
    def get_track_audio_features(self, track_ids):
        return self.send_authenticated_request(
            method="GET",
            url=f"{self.spotify_api_url}/audio-features/?ids={track_ids}",
        )

    # Get artist information
    def get_several_artists(self, artist_ids):
        return self.send_authenticated_request(
            method="GET",
            url=f"{self.spotify_api_url}/artists/?ids={artist_ids}",
        )
