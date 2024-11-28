# Spotify Download Automation

Automatically download new tracks added to a Spotify playlist via YouTube Music and save them to Google Cloud Storage.

## Features

- Monitors a specified Spotify playlist for newly added tracks
- Searches and downloads matching tracks from YouTube Music
- Converts downloaded tracks to MP3 format
- Uploads MP3 files to Google Cloud Storage
- Runs as a serverless Cloud Function

## Prerequisites

- Python 3.12+
- Poetry for dependency management
- Spotify API credentials
- Google Cloud Storage bucket
- Environment variables configured

## Installation

1. Clone the repository
2. Install dependencies using Poetry:

```sh
poetry install
```

3. Set up environment variables:

```sh
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_PLAYLIST_ID=your_playlist_id
```

## Usage

```sh
poetry run python src/main.py
```

The function will:

- Check for new tracks added to the Spotify playlist today.
- Download matching tracks from YouTube Music.
- Convert to MP3 format.
- Upload MP3 files to GCS bucket.
