import urllib.parse
import requests
import os

class Spotify:
    def __init__(self):
        self.CLIENT_ID = "875295a2f38d4725ab093fe2db5ebcbe"
        self.CLIENT_SECRET = "4dc3c3ab90da442caaa810c21ad4d376"
        self.REDIRECT_URI = 'http://127.0.0.1:5000/callback'
        self.auth_url = ''
        self.code= ''
        self.access_token = ''
        self.refresh_token = ''
        self.user_id = ''
        self.playlist_id = ''
        # self.authorize()
        self.top_items = ''
        self.logged_in = False


    def authorize(self):
        scopes = 'playlist-modify-public playlist-modify-private user-read-private user-read-email user-top-read'  # Add more scopes as needed
        auth_url = 'https://accounts.spotify.com/authorize'
        params = {
            "client_id": self.CLIENT_ID,
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URI,
            "scope": scopes
        }

        self.auth_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
        # print("Visit this URL to authorize the app:", self.auth_url)


    def get_bearer(self, code):

        with open("code.txt", 'w') as code_file:
            code_file.write(code)

        token_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.REDIRECT_URI,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET
        }

        response = requests.post(token_url, data=data)
        tokens = response.json()

        self.access_token = tokens.get("access_token")
        self.refresh_token = tokens.get("refresh_token")  # Save this for future use
        expires_in = tokens.get("expires_in")  # in seconds
        self.logged_in = True
        # print("Access Token:", self.access_token)
        # print("Refresh Token:", self.refresh_token)


    def refresh_access_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET
        }

        response = requests.post(token_url, data=data)
        tokens = response.json()

        if "access_token" in tokens:
            self.access_token = tokens["access_token"]
        else:
            raise Exception(f"Failed to refresh token: {tokens}")


    def get_user_id(self):
        header = {
            'Authorization': f"Bearer {self.access_token}",
        }
        response = requests.get(url= "https://api.spotify.com/v1/me", headers= header)
        print(response.json())

        self.user_id = response.json()['id']

    def get_top_items(self, top_type: str = "artists"):
        header = {
            'Authorization': f"Bearer {self.access_token}",
        }

        params = {
            "limit": 10,
            "time_range": "medium_term"
        }
        response = requests.get(url=f"https://api.spotify.com/v1/me/top/{top_type}", headers= header, params= params)
        self.top_items = response.json()

    def create_playlist(self, name):
        header = {
            'Authorization': f"Bearer {self.access_token}",
            'Content-Type': 'application/json',
        }

        body = {
            "name": name
        }

        response = requests.post(url= f"https://api.spotify.com/v1/users/{self.user_id}/playlists", headers= header, json= body)
        print(response.json())
        self.playlist_id = response.json()['id']

    def get_song(self, artist, song):
        endpoint = 'https://api.spotify.com/v1/search'

        header = {
            'Authorization': f"Bearer {self.access_token}",
        }

        query = f'artist:{artist} track:{song} '

        params = {
            'q': query,
            'type': 'track',
            'limit': 1,
            # 'market': 'GB'
        }

        response = requests.get(url= f"{endpoint}", params= params, headers= header)
        print(response.json())
        try:
            uri = response.json()['tracks']['items'][0]['uri']
        except IndexError:
            print("Index Error")
        else:
            self.add_to_playlist(uri)


    def add_to_playlist(self, uri):
        header = {
            'Authorization': f"Bearer {self.access_token}",
            'Content-Type': 'application/json',
        }

        body = {
            "uris": [uri]
        }

        response = requests.post(url=f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks", json=body, headers= header)
        print(response.text)