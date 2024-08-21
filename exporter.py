#! /usr/bin/env python3
import exporter_xlsx
from helpers import sanitize

import spotipy
import config
import csv
from spotipy.oauth2 import SpotifyOAuth
from argparse import ArgumentParser

def export_albums_csv(sp):
    # prepare output CSV file
    out = open("saved_albums.csv", "w", newline="")
    csvfile = csv.writer(out)
    fields = ["Title", "Artist(s)", "Spotify Link"]
    csvfile.writerow(fields)

    # get all saved albums and write to CSV
    albums = sp.current_user_saved_albums()
    while albums:
        for i, item in enumerate(albums['items']):
            row = []
            row.append(sanitize(item['album']['name']))
            # append artists as comma-separated list
            artists = sanitize(item['album']['artists'][0]['name'])
            for ar in item['album']['artists'][1:]:
                artists += ", " + sanitize(ar['name'])
            row.append(artists)
            row.append(item["album"]["external_urls"]["spotify"])
            csvfile.writerow(row)

        if albums['next']:
            albums = sp.next(albums)
        else:
            albums = None

    out.close()

def main():
    # parse args
    parser = ArgumentParser()
    # parser.add_argument("-p", "--playlists", action="store_true", help="Export user playlists.")
    parser.add_argument("-a", "--albums", action="store_true", help="Export user saved albums to CSV.")
    parser.add_argument("--albums_xlsx", action="store_true", help="Export user saved albums to Excel file with images.")
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
        export_albums_csv(sp)
    elif args.albums_xlsx:
        # exporter_xlsx.export_albums_xlsx(sp)
        print("TODO")

    else:
        print("Use --albums to export user saved albums to CSV")

if __name__ == '__main__':
    main()
