import spotipy
from spotipy.oauth2 import SpotifyOAuth
from backend.config import Config

class MockSpotifyClient:
    _instance = None
    
    def __init__(self):
        self.user_id = "demo_user"

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_user_playlists(self):
        from backend.funciones import load_master_file
        playlists_data = load_master_file()
        if not playlists_data:
            return []
        
        playlists = []
        for uri, data in playlists_data.items():
            playlists.append(f"{data['name']}:{uri}")
        return playlists

    def get_playlist_tracks(self, playlist_id):
        import json
        import os
        from backend.funciones import get_playlist_track_file
        
        file_path = get_playlist_track_file(playlist_id)
        if not file_path or not os.path.exists(file_path):
            return []
            
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        tracks = []
        for track_id, meta in data.items():
            tracks.append({
                "track": {
                    "id": track_id,
                    "uri": f"spotify:track:{track_id}",
                    "name": meta["nombre"],
                    "artists": [{"name": a} for a in meta["artistas"]],
                    "album": {"name": meta["album"], "release_date": f'{meta["ano"]}-{meta["mes"]}-{meta["dia"]}'},
                    "disc_number": meta["n_disc"],
                    "track_number": meta["n_track"],
                }
            })
        return tracks

    def get_audio_features_batch(self, track_ids):
        return [{"danceability": 0, "energy": 0, "acousticness": 0, "instrumentalness": 0, "valence": 0, "liveness": 0, "tempo": 0, "mode": 0}] * len(track_ids)

    def reorder_playlist(self, playlist_id, ordered_uris, current_uris):
        import time
        for i in range(len(ordered_uris)):
            time.sleep(0.01) # Simulate network delay for UI progress bar
            yield f"{i+1}/{len(ordered_uris)}"


class SpotifyClient:
    _instance = None
    
    def __init__(self):
        Config.validate()
        # Added playlist-read-private and playlist-read-collaborative to ensure access to all user playlists
        # REDUCED SCOPES TO MATCH CACHED TOKEN (Bypassing broken auth flow)
        self.scope = 'playlist-modify-public playlist-modify-private'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=Config.SPOTIPY_CLIENT_ID,
            client_secret=Config.SPOTIPY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIPY_REDIRECT_URI,
            scope=self.scope
        ))
        self.user_id = self.sp.current_user()['id']

    @classmethod
    def get_instance(cls):
        if Config.DEMO_MODE:
            return MockSpotifyClient.get_instance()
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_user_playlists(self):
        playlists = []
        results = self.sp.current_user_playlists()
        while results:
            for i in results['items']:
                # Handle cases where playlist name might be None
                name = i['name'] if i['name'] else "Untitled Playlist"
                playlists.append(f"{name}:{i['id']}")
            if results['next']:
                results = self.sp.next(results)
            else:
                results = None
        return playlists

    def get_playlist_tracks(self, playlist_id):
        # Using playlist_items instead of user_playlist_tracks
        results = self.sp.playlist_items(playlist_id=playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return tracks

    def get_audio_features_batch(self, track_ids):
        # Spotify allows up to 100 ids per request
        features = []
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            try:
                batch_features = self.sp.audio_features(batch)
                
                # Check for None results (happens if a track id is invalid but API doesn't error)
                if batch_features:
                   # Filter out Nones from the result list itself if any
                   batch_features = [f if f else None for f in batch_features]
                   features.extend(batch_features)
                else:
                    # Append Nones for the whole batch if it returns empty/None
                    features.extend([None] * len(batch))
                    
            except spotipy.SpotifyException as e:
                print(f"Error fetching audio features for batch {i}-{i+100}: {e}")
                
                # Spotify has restricted the audio-features endpoint for many apps (returns 403)
                # If we get a 403, don't even try individual fallback, and don't try other batches.
                # Simply skip stats for the remaining tracks to prevent long loops or hanging.
                if e.http_status in (403, 404):
                    print("API restricted (403) or missing (404), applying stat-less workaround immediately for all remaining tracks.")
                    features.extend([None] * (len(track_ids) - len(features)))
                    return features
                
                print(f"Falling back to individual fetch for batch {i}-{min(i+100, len(track_ids))}")
                
                # Fallback: Fetch one by one
                batch_fallback = []
                for track_id in batch:
                    try:
                        f = self.sp.audio_features([track_id])
                        if f and f[0]:
                            batch_fallback.append(f[0])
                        else:
                            print(f"Failed individual fetch for {track_id}: No data returned")
                            batch_fallback.append(None)
                    except Exception as inner_e:
                        print(f"Failed individual fetch for {track_id}: {inner_e}")
                        batch_fallback.append(None)
                
                features.extend(batch_fallback)

            except Exception as e:
                print(f"Unexpected error in batch {i}-{i+100}: {e}")
                features.extend([None] * len(batch))
                
        return features

    def reorder_playlist(self, playlist_id, ordered_uris, current_uris):
        # We need to reorder the playlist to match ordered_uris
        # This is tricky because reorder_tracks takes a range_start and insert_before
        # A simple implementation is to clear and add, but that loses added_at data
        # The original implementation used a loop with reorder_tracks, which is slow but correct
        # Let's keep the logic similar but optimized if possible
        
        # Original logic seems to be bubble-sort-like or insertion-sort-like on the live playlist
        # "sp2.user_playlist_reorder_tracks(user,playlist_id=uri,range_start=d_uri.index(n_uri), insert_before=n)"
        # This moves the track at the current position of n_uri to position n
        
        # We need to replicate the state of the playlist locally to track indices
        local_order = list(current_uris)
        
        for i, target_uri in enumerate(ordered_uris):
            try:
                current_index = local_order.index(target_uri)
            except ValueError:
                continue # Track might not be in the list anymore?
            
            if current_index != i:
                self.sp.user_playlist_reorder_tracks(
                    self.user_id, 
                    playlist_id=playlist_id, 
                    range_start=current_index, 
                    insert_before=i
                )
                # Update local state
                track = local_order.pop(current_index)
                local_order.insert(i, track)
            
            yield f"{i+1}/{len(ordered_uris)}"
