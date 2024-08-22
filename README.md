# Spotify Data Exporter

This script allows you to export metadata from your Spotify account, specifically files listing your saved albums and playlists. To use it, you must create your own app on [developer.spotify.com](https://developer.spotify.com), and provide your app's client ID and secret.

## Setup

This project primarily relies on the [Spotipy](spotipy.readthedocs.io) library to make calls to the Spotify WebAPI. 
- Install requirments with `pip install -r requirements.txt`
- Create Spotify Developer App with redirect URI `https://localhost:8000/callback/`
- Add `client_id` and `client_secret` to `config.py`

## Usage

### Export Your Saved Albums to CSV

Export user saved albums list to a CSV file by running
```
./exporter.py --albums
```
When run initially, your web browser will be opened for you to log in to Spotify. Paste the URL from web broswer when prompted once you've logged in.

### Export Your Playlists

To export your public playlists, run the following command:

```
./exporter.py --playlists
```

For each playlist, this will produce a folder named after the playlist (if the playlist's name only contains special characters, the folder generated will be named by the playlist's ID). The folder will contain:

- The playlist's cover image
- `playlist_name.txt` which contains the original name of the playlist
- `tracks.csv` which contains a list of tracks, including their title, artist(s), album, release date, date added to playlist, and their Spotify URLs

This function will only output the playlists that are public/on your profile. If you want to export private playlists, create a `.txt` file listing your playlists and use the following command.

#### Export Playlists from File

To export playlists from a custom list, create a `.txt` file where each line contains the Spotify URL to each playlist. Then run the following command, providing the path to the file:

```
./exporter.py --playlist_file <playlist_file_path>
```

Since you will be authenticated to the Spotify API, you are able to export your private playlists using this command, if their URLs are included in your list. You can also include any other public playlists you wish to export.

#### Export Playlist to CSV from URL

Run the following command, providing the `<playlist_url>` from Spotify, to export an individual playlist:

```
./exporter.py --playlist_url <playlist_url>
```

You may want to provide the playlist url in quotation marks (e.g. `./exporter.py --playlist_url "https://open.spotify.com/playlist/..."`) to prevent issues with special characters in the command line
