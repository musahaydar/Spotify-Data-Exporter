# Spotify Data Exporter

This script allows you to export metadata from your Spotify account. To use it, you must create your own app on [developer.spotify.com](https://developer.spotify.com), and provide your app's client ID and secret.

## Setup

This project primarily relies on the [Spotipy](spotipy.readthedocs.io) library to make calls to the Spotify WebAPI. 
- Install requirments with `pip install -r requirements.txt`
- Create Spotify Developer App with redirect URI `https://localhost:8000/callback/`
- Add `client_id` and `client_secret` to `config.py`

## Usage

### Export Saved Albums to CSV

Export user saved albums list to a CSV file by running
```
./exporter.py --albums
```
When run initially, your web browser will be opened for you to log in to Spotify. Paste the URL from web broswer when prompted once you've logged in.

### Export Playlist to CSV from URL

```
./exporter.py --playlist_url <playlist_url>
```

Run this command, providing the `<playlist_url>` from Spotify, to export a playlist to a single CSV. This will produce a folder named after the playlist (if the playlist's name only contains special characters, the folder generated will be named by the playlist's ID). The folder will contain:

- The playlist's cover image
- `playlist_name.txt` which contains the original name of the playlist
- `tracks.csv` which contains a list of tracks, including their title, artist(s), album, release date, date added to playlist, and their Spotify URLs
