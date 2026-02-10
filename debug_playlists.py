from backend.spotify_call import SpotifyClient
import sys

def debug():
    print("Initializing Authentication...")
    from spotipy.oauth2 import SpotifyOAuth
    from backend.config import Config
    
    # Initialize auth manager manually to handle headless auth if needed
    auth_manager = SpotifyOAuth(
        client_id=Config.SPOTIPY_CLIENT_ID,
        client_secret=Config.SPOTIPY_CLIENT_SECRET,
        redirect_uri=Config.SPOTIPY_REDIRECT_URI,
        # We need the same scopes as SpotifyClient
        scope='playlist-modify-public playlist-modify-private',
        open_browser=False
    )
    
    # Check if token is already valid
    token_info = auth_manager.get_cached_token()
    if not auth_manager.validate_token(token_info):
        # Need to auth
        auth_url = auth_manager.get_authorize_url()
        print(f"\nPLEASE AUTHORIZE HERE: {auth_url}\n")
        
        # We can't interactively ask user here easily without blocking/timeout issues in some envs,
        # but since we are running this in a terminal, we can try input().
        # However, the Agent tool validation might time out if we wait too long.
        # Better approach: Print URL and ask user to paste the REDIRECTED URL.
        
        print("Waiting for user to paste the redirected URL...")
        response = input("Paste the full redirected URL here: ")
        
        code = auth_manager.parse_response_code(response)
        auth_manager.get_access_token(code)
        print("Authentication successful!")
    
    print("Initializing SpotifyClient...")
    try:
        client = SpotifyClient.get_instance()
    except Exception as e:
        print(f"Failed to initialize client: {e}")
        return

    print("Fetching playlists...")
    playlists = client.get_user_playlists()
    
    print(f"Found {len(playlists)} playlists.")
    
    for pl_str in playlists:
        try:
            name, pid = pl_str.split(':')
            # Only debug if it looks like a test or the user mentioned "previous playlist" failure.
            # We'll just scan the first 3 to avoid spam, or finding one with many tracks.
            print(f"\nScanning Playlist: {name} ({pid})")
            
            # Use the existing method to see if it works/fails
            tracks = client.get_playlist_tracks(pid)
            print(f"  Total items returned: {len(tracks)}")
            
            if not tracks:
                print("  [WARN] No tracks returned.")
                continue

            invalid_count = 0
            valid_count = 0
            
            # Check the first 5 tracks in detail
            for i, item in enumerate(tracks[:5]):
                track = item.get('track')
                if not track:
                    print(f"    Item {i}: Track object is None/Empty. Raw item keys: {item.keys()}")
                    invalid_count += 1
                    continue
                
                tid = track.get('id')
                tname = track.get('name', 'Unknown')
                if not tid:
                    print(f"    Item {i}: Track '{tname}' has NO ID. Is Local: {track.get('is_local')}, Type: {track.get('type')}")
                    invalid_count += 1
                else:
                    valid_count += 1
                    # Try fetching features for this specific track
                    try:
                        features = client.sp.audio_features([tid])
                        if features and features[0]:
                            print(f"    Item {i}: '{tname}' (ID: {tid}) -> Features OK")
                        else:
                            print(f"    Item {i}: '{tname}' (ID: {tid}) -> Features FAILED (None)")
                    except Exception as e:
                        print(f"    Item {i}: '{tname}' (ID: {tid}) -> Features EXCEPTION: {e}")

            print(f"  ... checked first 5. (Valid: {valid_count}, Invalid/NoID: {invalid_count} in sample)")

        except Exception as e:
            print(f"  Error processing playlist {pl_str}: {e}")

if __name__ == "__main__":
    debug()
