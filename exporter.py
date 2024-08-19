#! /usr/bin/env python3
import spotipy
import config
from spotipy.oauth2 import SpotifyOAuth
from argparse import ArgumentParser

def export_albums(sp):
    albums = sp.current_user_saved_albums()
    while albums:
        for i, item in enumerate(albums['items']):
            print(item['album']['artists'][0]['name'] + " - " + item['album']['name'])
        if albums['next']:
            albums = sp.next(albums)
        else:
            albums = None

def main():
    # parse args
    parser = ArgumentParser()
    # parser.add_argument("-p", "--playlists", action="store_true", help="Export user playlists.")
    parser.add_argument("-a", "--albums", action="store_true", help="Export user saved albums.")
    args = parser.parse_args()

    # connect to spotify and authenticate
    scope = "user-library-read"
    auth = SpotifyOAuth(
        client_id=config.client_id,
        client_secret=config.client_secret,
        scope=scope,
        redirect_uri=config.redirect_uri)
    sp = spotipy.Spotify(auth_manager=auth)
    # this will cause the login prompt to open and also get user info
    user = sp.current_user()

    if args.albums:
        export_albums(sp)

    else:
        print("Use --albums to export user saved albums")

if __name__ == '__main__':
    main()