from datetime import datetime
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from google.cloud import storage
import functions_framework

load_dotenv()
auth_manager = SpotifyClientCredentials()

spotify_client = sp = spotipy.Spotify(auth_manager=auth_manager)
ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }
    ],
    "keepvideo": False,
    "postprocessor_args": ["-metadata", "title=%(track)s"],
    "embedmetadata": True,
    "embedthumbnail": True,
    "outtmpl": "/tmp/%(title)s.%(ext)s",
}
yt_dl_client = YoutubeDL(ydl_opts)
storage_client = storage.Client()
bucket_name = "spotify-music-bucket"
bucket = storage_client.get_bucket(bucket_name)


def get_new_playlist_items():
    """
    Fetches the list of tracks added to a Spotify playlist on the current date.

    Returns:
        list: A list of track names in the format "Artist - Track Name".
    """
    playlist_id = os.getenv("SPOTIFY_PLAYLIST_ID")
    current_date = datetime.now().strftime("%Y-%m-%d")
    limit = 100
    offset = 0
    new_tracks = []

    while True:
        # Fetch playlist items with pagination
        response = spotify_client.playlist_items(
            playlist_id, limit=limit, offset=offset
        )
        items = response.get("items", [])

        # Break the loop if there are no more items
        if not items:
            break

        # Filter tracks by the added date
        for item in items:
            track = item.get("track")
            if not track:
                continue

            added_date = item.get("added_at", "").split("T")[0]
            if added_date == current_date:
                artist = track["artists"][0]["name"]
                track_name = track["name"]
                new_tracks.append(f"{artist} - {track_name}")

        offset += limit

    return new_tracks


def find_youtube_music_title(title):
    """
    Fetches the YouTube Music URL for a given track.

    Args:
        title (str): The title of the track in the format "Artist - Track Name".
    """
    yt_dl_client.extract_info(f"ytsearch:{title}", download=True)


def save_to_gcs():
    """
    Downloads a track from YouTube Music and saves it to Google Cloud Storage.

    Args:
        url (str): The YouTube Music URL for the track.

    Returns:
        str: The Google Cloud Storage URL for the track.
    """

    # upload all mp3 files in /tmp to GCS
    for file in os.listdir("/tmp"):
        if file.endswith(".mp3"):
            blob = bucket.blob(file)
            blob.upload_from_filename(f"/tmp/{file}")


@functions_framework.http
def main(request):
    new_items = get_new_playlist_items()
    for item in new_items:
        find_youtube_music_title(item)
    save_to_gcs()
