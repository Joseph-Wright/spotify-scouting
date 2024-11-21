# import spotipy
# # from spotipy.oauth2 import SpotifyClientCredentials
# from spotipy.oauth2 import SpotifyOAuth
# # import random
# # import json
# import os
# # from time import time


# CLIENT_ID = os.env.get("CLIENT_ID")
# CLIENT_SECRET = os.env.get("CLIENT_SECRET")
# MARKET = "GB"
# GENRES = ["indie-pop", "indie", "alt-rock", "alternative"]
# SEED_TRACKS = []
# SEED_PLAYLIST = "https://open.spotify.com/playlist/03w9EPuK6oCz7VaKd2wM0U?si=374cf2f2a4b94107"
# OUTPUT_PLAYLIST = "https://open.spotify.com/playlist/2kWTxfXaMscnx0EFq87phv?si=20ea8a00aa90433b"
# TARGET_POPULARITY = 0

# class SpotifyService:
#     def __init__(self, redirect_url):
#         # sp = spotipy`.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
#         self.sp = spotipy.Spotify(
#             auth_manager=SpotifyOAuth(
#                 client_id=CLIENT_ID,
#                 client_secret=CLIENT_SECRET,
#                 redirect_uri=redirect_url,
#                 scope="playlist-modify-private"
#             )
#         )

#         seed_tracks = sp.playlist_items(SEED_PLAYLIST)

#         seed_artists = []
#         for i in seed_tracks["items"]:
#             seed_artists.append(i["track"]["artists"][0]["uri"].split(":")[-1])

#         seed_tracks = [t["track"]["external_urls"]["spotify"] for t in seed_tracks["items"]]