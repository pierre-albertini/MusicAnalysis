import spotipy
from musicbrainzngs import NetworkError
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import time
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import ssl
import certifi
import musicbrainzngs

# Setup SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Set up MusicBrainz
musicbrainzngs.set_useragent(
    "MusicAnalysis",
    "1.0",
    "pierrealbertini@icloud.com"
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response_code = self.path.split("?code=")[-1]
        self.wfile.write(f"<html><body><h1>Authorization code received.</h1><p>{response_code}</p></body></html>".encode('utf-8'))
        self.server.auth_code = response_code

def run_server():
    server_address = ('', 8088)
    httpd = HTTPServer(server_address, SpotifyAuthHandler)
    httpd.handle_request()
    return httpd.auth_code

class SpotifyData:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        self.scope = os.getenv("SPOTIFY_SCOPE",
                               "user-library-read user-read-private playlist-read-private user-top-read")
        self.sp = None
        self.user_data = {
            "username": "",
            "userid": "",
            "country": "",
            "profile_picture": "",
            "num_playlists": 0,
            "num_tracks": 0,
            "num_liked_tracks": 0,
            "top_genres": [],
            "favorite_songs": []
        }
        self.set_up_Spotify()

    def set_up_Spotify(self):
        sp_oauth = SpotifyOAuth(client_id=self.client_id,
                                client_secret=self.client_secret,
                                redirect_uri=self.redirect_uri,
                                scope=self.scope)

        try:
            token_info = sp_oauth.get_cached_token()
            if not token_info:
                auth_url = sp_oauth.get_authorize_url()
                print("Please visit the following URL to authorize the application:")
                print(auth_url)

                response_code = run_server()
                token_info = sp_oauth.get_access_token(response_code)

            access_token = token_info['access_token']
            self.sp = spotipy.Spotify(auth=access_token)
            return self.sp

        except spotipy.oauth2.SpotifyOauthError as e:
            logging.error(f"Spotify OAuth Error: {e}")
            return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    def get_user_data(self):
        if not self.sp:
            logging.error("Spotify client is not set up.")
            return

        user = self.sp.current_user()
        self.user_data["username"] = user["display_name"]
        self.user_data["userid"] = user["id"]
        self.user_data["country"] = user["country"]
        self.user_data["profile_picture"] = user["images"][0]["url"] if user["images"] else ""

        playlists = self.sp.current_user_playlists(limit=20)
        self.user_data["num_playlists"] = playlists["total"]

        tracks = self.sp.current_user_saved_tracks()
        self.user_data["num_tracks"] = tracks["total"]

        liked_tracks = self.sp.current_user_saved_tracks(limit=50)
        self.user_data["num_liked_tracks"] = liked_tracks["total"]

        top_artists = self.sp.current_user_top_artists(limit=10, time_range="short_term")
        self.user_data["top_genres"] = [artist["genres"] for artist in top_artists["items"]]

    def get_favorite_songs(self):
        if not self.sp:
            logging.error("Spotify client is not set up.")
            return

        start_time = time.time()
        favorite_songs = []
        limit = 50
        offset = 0
        artist_cache = {}

        while len(favorite_songs) < self.user_data["num_liked_tracks"]:
            tracks = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
            for track in tracks["items"]:
                track_info = track["track"]
                track_name = track_info["name"]
                artist_name = track_info["artists"][0]["name"]
                track_id = track_info["id"]
                added_at = track["added_at"]
                track = self.sp.track(track_id)
                track_duration = track["duration_ms"]
                album_id = track_info["album"]["id"]
                album = self.sp.album(album_id)
                album_name = album["name"]
                release_date = album["release_date"]

                if artist_name in artist_cache:
                    artist_country = artist_cache[artist_name]

                else:
                    try:
                        artist_info = musicbrainzngs.search_artists(
                            artist=artist_name,
                            limit=1
                        )
                        time.sleep(1)

                        artist_country = (
                            artist_info["artist-list"][0].get("country", "Unknown")
                            if artist_info.get("artist-list")
                            else "Unknown"
                        )

                    except NetworkError:
                        # 🔹 Spotify fallback
                        try:
                            spotify_artist_id = track_info["artists"][0]["id"]
                            spotify_artist = self.sp.artist(spotify_artist_id)

                            artist_country = (
                                spotify_artist.get("genres", ["Unknown"])[0]
                                if spotify_artist.get("genres")
                                else "Unknown"
                            )
                        except Exception:
                            artist_country = "Unknown"

                    # Cache result
                    artist_cache[artist_name] = artist_country

                favorite_songs.append(
                    (track_name, artist_name, track_id, album_name, track_duration, release_date, artist_country, added_at))
                logging.info(f"Processed {track_name} by {artist_name}, added on {added_at}")

            offset += limit

        self.user_data["favorite_songs"] = favorite_songs
        self.save_data("./JSON_files/RawDataSpotify.json", self.user_data)
        self.save_data("./JSON_files/OrderedDataSpotify.json", self.format_data_for_output())

        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Favorite songs retrieval took {execution_time} seconds.")

    def save_data(self, filepath, data):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

    def format_data_for_output(self):
        formatted_songs = [{"name": f"\n{song[0]} - {song[1]} - {song[2]} - {song[3]} - {song[4]} - {song[5]}"} for song in self.user_data["favorite_songs"]]
        output_data = self.user_data.copy()
        output_data["favorite_songs"] = formatted_songs
        return output_data

    def load_spotify_favorite_songs(self):
        data_file_path = "./JSON_files/RawDataSpotify.json"
        if os.path.exists(data_file_path):
            with open(data_file_path, "r") as file:
                data = json.load(file)

            self.user_data = data
            print("Data successfully loaded")
        else:
            logging.info("No data file found, please initialize data")