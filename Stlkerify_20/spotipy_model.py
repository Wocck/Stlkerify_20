import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import re

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI))


def parse_user_url(url):
    try:
        pattern = r'user/([^?/]+)'
        matches = re.search(pattern, url)
        return matches.group(1)
    except Exception as e:
        print(e)
        return None


def parse_track_url(url):
    try:
        pattern = r'track/([^?/]+)'
        matches = re.search(pattern, url)
        return matches.group(1)
    except Exception as e:
        print(e)
        return None


def get_track_id(track_name, artist_name):
    try:
        query = f'track:{track_name} artist:{artist_name}'
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']
            return track_id
        else:
            return -1
    except Exception as e:
        print(e)
        return None


def search_by_track_id(user_id, track_id):
    track = sp.track(track_id)
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    try:
        playlists = sp.user_playlists(user_id)
        for playlist in playlists['items']:
            fields = "items.track.id, items.track.name, items.track.artists.name"
            results = sp.playlist_items(playlist['id'], fields=fields)
            for item in results['items']:
                if track_id == item['track']['id']:
                    return True, playlist['name'], item['track']['name'], item['track']['artists'][0]['name'], user_id
        return False, None, track_name, artist_name, user_id
    except Exception as e:
        print(e)
        return None


def search_tracks_by_name_artist(track_name, artist_name):
    try:
        query = f'track:{track_name} artist:{artist_name}'
        results = sp.search(q=query, type='track', limit=6)
        tracks = results['tracks']['items']
        search_results = []
        for track in tracks:
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            images = track['album']['images']
            if images:
                track_photo = images[0]['url']
            else:
                track_photo = None
            search_results.append({
                'track_id': track_id,
                'track_name': track_name,
                'artist_name': artist_name,
                'track_photo': track_photo
            })
        return search_results
    except Exception as e:
        print(e)
        return None


def get_user_name(user_id):
    try:
        user = sp.user(user_id)
        return user['display_name']
    except Exception as e:
        print(e)
        return None
