from backend.spotify_call import SpotifyClient
from backend.funciones import create_playlist_json, get_track_data

def test():
    client = SpotifyClient.get_instance()
    
    # Just grab the first playlist to test the stat-less workaround fetching behavior
    playlists = client.get_user_playlists()
    if not playlists: return
    name, uri = playlists[0].split(':')
    
    print(f"Testing playlist: {name}")
    try:
        raw_tracks = client.get_playlist_tracks(uri)
        print(f"  -> RAW TRACKS from API: {len(raw_tracks)}")
        
        tracks = get_track_data(uri)
        print(f"  -> Got {len(tracks)} tracks")
        if len(tracks) == 0:
            print(f"  -> EMPTY RESULTS!")
        else:
            print(f"  -> FIRST TRACK PROCESSED SUCCESSFULLY: {tracks[0][:2]}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"  -> CRASHED: {e}")

if __name__ == "__main__":
    test()
