from typing import Optional
import spotipy
from spotipy.cache_handler import CacheFileHandler
from models.errors import NotSignedIn
from utils.spotify_auth import CustomAuth
# import random
# import json
import os
# from time import time
from models.models import SubmitRequest

class SpotifyService:
    def __init__(self, redirect_url="http://192.168.0.200:8000/callback", token=None):
        print("initialsiseing spot svc")
        self.cache_handler = CacheFileHandler(username=token)
        self.auth = CustomAuth(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            redirect_uri=redirect_url,
            scope="playlist-modify-private playlist-read-private",
            show_dialog=True,
            open_browser=False,
            cache_handler=self.cache_handler
        )
        self.sp = spotipy.Spotify(
            auth_manager=self.auth
        )
        self.me = None
        self.market = "GB"

    def get_user_id(self):
        if not self.me:
            self.me = self.sp.me()["id"]
        return self.me

    def submit_playlist(self, params: SubmitRequest):
        seed_artists = []
        seed_tracks = None

        input_playlist = self.sp.playlist(params.userInput)
        output_playlist_name = input_playlist["name"] + (
            "_artist" if params.byArtist else "_tracks"
        )
        playlist_id = self.upsert_playlist(output_playlist_name)

        output_playlist_items = self.sp.playlist_items(playlist_id)
        existing_artists = set()
        for track in output_playlist_items["items"]:
            existing_artists.update([a["id"] for a in track["track"]["artists"]])

        seed_track_response = self.sp.playlist_items(params.userInput)

        if params.byArtist:
            for i in seed_track_response["items"]:
                seed_artists.append(i["track"]["artists"][0]["uri"].split(":")[-1])
        else:
            seed_tracks = [t["track"]["external_urls"]["spotify"] for t in seed_track_response["items"]]

        del seed_track_response

        results = self.sp.recommendations(
            country=self.market,
            limit=100,
            seed_tracks=seed_tracks,
            seed_artists=seed_artists,
            **params.sliderValues.model_dump()
        )
        tracks = []
        print(len(results["tracks"]), "recommendations")
        for result in results["tracks"]:
            artist_id = result["artists"][0]["id"]
            artist = self.sp.artist(artist_id)
            name = result["artists"][0]["name"]
            followers = artist["followers"]["total"]
            link = result["external_urls"]["spotify"]
            if followers < 2500 and artist_id not in existing_artists:
                albums = self.get_albums(artist_id=artist_id)
                dates = [int(a["release_date"][:4]) for a in albums if a["release_date"]]
                if not dates or min(dates) >= 2022:
                    print(name)
                    print(followers, "followers")
                    print(link)
                    print()
                    tracks.append(link)
                    existing_artists.add(artist_id)
        if tracks:
            self.sp.playlist_add_items(playlist_id, tracks)

    def upsert_playlist(self, playlist_name):
        playlists = self.get_playlists()
        filtered_playlists = [
            playlist
            for playlist
            in playlists
            if playlist_name == playlist["name"]
        ]
        if len(filtered_playlists) > 1:
            raise Exception(f"duplicate playlists with name {playlist_name}")
        elif len(filtered_playlists) == 1:
            return filtered_playlists[0]["id"]
        else:
            return self.sp.user_playlist_create(
               self.get_user_id(),
               playlist_name,
               public=False,
               collaborative=False,
               description=''
            )["id"]

    def get_playlists(self):
        def recur_response(response):
            items = response["items"]
            if response["next"]:
                items += recur_response(self.sp.next(response))
            return items
        playlists = recur_response(self.sp.user_playlists(self.get_user_id()))
        return playlists

    def get_albums(self, artist_id: str):
        def recur_response(response):
            items = response["items"]
            if response["next"]:
                items += recur_response(self.sp.next(response))
            return items
        albums = recur_response(self.sp.artist_albums(artist_id=artist_id))
        return albums

class SpotifyHandler:
    def __init__(self):
        self.instances = {}
        return

    def create_instance(self, token: str):
        self.instances[token] = SpotifyService(token=token)
        return self.instances[token]

    def get_instance(self, token: str):
        if token not in self.instances:
            raise NotSignedIn()
        return self.instances[token]

spotify_handler = SpotifyHandler()
