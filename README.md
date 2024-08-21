# Spotify Data Exporter

This script allows you to export metadata from your Spotify account. To use it, you must create your own app on [developer.spotify.com](https://developer.spotify.com), and provide your app's client ID and secret.

## Setup

This project primarily relies on the [Spotipy](spotipy.readthedocs.io) library to make calls to the Spotify WebAPI. 
- Install requirments with `pip install -r requirements.txt`
- Create Spotify Developer App with callback `https://localhost:8000/callback/`
- Add `client_id` and `client_secret` to `config.py`

## Usage

Export user saved albums list to a CSV file by running
```
./exporter.py --albums
```
When run initially, your web browser will be opened for you to log in to Spotify. Paste the URL from web broswer when prompted once you've logged in.
