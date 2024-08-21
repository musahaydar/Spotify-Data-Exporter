#! /usr/bin/env python3
import exporter_xlsx
from helpers import *

import spotipy
import config
import csv
import re
from spotipy.oauth2 import SpotifyOAuth
from argparse import ArgumentParser
from pathlib import Path
from urllib.request import urlretrieve

def export_albums_csv(sp):
    # prepare output CSV file
    out = open("saved_albums.csv", "w", newline="")
    csvfile = csv.writer(out)
    fields = ["Title", "Artist(s)", "Released", "Spotify Link"]
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
            row.append(item["album"]["release_date"])
            row.append(item["album"]["external_urls"]["spotify"])
            csvfile.writerow(row)

        if albums['next']:
            albums = sp.next(albums)
        else:
            albums = None

    out.close()

def export_playlist_url(sp, url):
    # get the ID out of the URL and calls export_playlist_id
    id = re.search("\/.*\/(.*)\?", url)

    if id is None:
        print("Error: please enter a valid Spotify URL")
        return
    
    export_playlist_id(sp, id.group(1))

def export_playlist_id(sp, id):
    name = sp.playlist(id)["name"]
    filename = make_name_safe(name)
    if filename == "": 
        filename = id

    # create output dir
    Path(filename).mkdir(exist_ok=True)
    dir = Path(filename)

    # save cover image to file
    urlretrieve(sp.playlist_cover_image(id)[0]["url"], dir/Path(filename + ".jpg"))

    # write playlist name to a file
    with open(dir/Path("playlist_name.txt"), "a") as f:
        f.write(name + "\n")
    
    # retrieve songs as CSV file
    out = open(dir/Path("tracks.csv"), "w", newline="")
    csvfile = csv.writer(out)
    fields = ["Track", "Artist(s)", "Album", "Released", "Date Added", "Spotify Link"]
    csvfile.writerow(fields)

    tracks = sp.playlist_items(id)
    while tracks:
        for i, item in enumerate(tracks['items']):
            row = []
            row.append(sanitize(item['track']['name']))
            # append artists as comma-separated list
            artists = sanitize(item['track']['artists'][0]['name'])
            for ar in item['track']['artists'][1:]:
                artists += ", " + sanitize(ar['name'])
            row.append(artists)
            row.append(sanitize(item["track"]["album"]["name"]))
            row.append(item["track"]["album"]["release_date"])
            row.append(item["added_at"])
            row.append(item["track"]["external_urls"]["spotify"])
            csvfile.writerow(row)

        if tracks['next']:
            tracks = sp.next(tracks)
        else:
            tracks = None

    out.close()

def main():
    # parse args
    parser = ArgumentParser()

    # playlist arguments
    parser.add_argument("-p", "--playlists", action="store_true", help="Export user playlists.")
    parser.add_argument("--playlist_url", type=str, default="")

    # album arguments
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

    # some args are only allowed when others are not used, and that's determined by the if-else flow here
    if args.albums:
        export_albums_csv(sp)
    elif args.albums_xlsx:
        # exporter_xlsx.export_albums_xlsx(sp)
        print("TODO")
    
    if args.playlists:
        print("TODO")
    elif args.playlist_url:
        export_playlist_url(sp, args.playlist_url)

    else:
        print("Use --albums to export user saved albums to CSV")

if __name__ == '__main__':
    main()
