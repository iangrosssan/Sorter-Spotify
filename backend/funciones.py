import os, json
from backend.spotify_call import SpotifyClient

CACHE_DIR = "backend/attribute_cache"

# JSON playlists
def guardar_playlists(playlists):
    data = {
        uri: {'name': name, 'tracks_file': f'{CACHE_DIR}/{uri}.json'} for name, uri in [i.split(':') for i in playlists]
    }
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(f'{CACHE_DIR}/playlists.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def get_track_data(uri):
    playlist_file_path = get_playlist_track_file(uri)
    if not os.path.isfile(playlist_file_path):
        create_playlist_json(uri)

    # Need to load it again, it might have just been created
    with open(playlist_file_path, 'r', encoding='utf-8') as playlist_file:
        track_metadata = json.load(playlist_file)
        
    # If the cache is completely empty but the file exists, it might be poisoned from a previous failure.
    if not track_metadata:
        create_playlist_json(uri)
        with open(playlist_file_path, 'r', encoding='utf-8') as playlist_file:
            track_metadata = json.load(playlist_file)

    l_tracks = []
    # We load tracks from the cache, but we should make sure they are in order of the LIVE playlist
    # or just return the cached data. The original function fetched live tracks again.
    # To be consistent with "displaying current state", let's load live tracks order.
    client = SpotifyClient.get_instance()
    tracks = client.get_playlist_tracks(uri)
    
    for item in tracks:
        track = item['track']
        if not track: continue # Handle local files or null tracks
        
        track_uri = track['uri'].split(':')[2]
        if track_uri not in track_metadata:
            continue
            
        meta = track_metadata[track_uri]
        
        info_track = [
            track_uri,
            meta['nombre'],
            meta['n_disc'],
            meta['n_track'],
            meta['album'],
            meta['ano'],
            meta['mes'],
            meta['dia'],
            meta['artistas'],
            meta['danceability'],
            meta['energy'],
            meta['acousticness'],
            meta['instrumentalness'],
            meta['valence'],
            meta['liveness'],
            meta['tempo'],
            meta['mode']
        ]
        l_tracks.append(info_track)
    return l_tracks

def average_metadata(tracks_data):
    if not tracks_data:
        return {}
    
    # Indices based on info_track above:
    # dance: 9, energy: 10, acoustic: 11, instrumental: 12, valence: 13
    count = len(tracks_data)
    return {
        'dance': sum(t[9] for t in tracks_data) / count,
        'energy': sum(t[10] for t in tracks_data) / count,
        'acoustic': sum(t[11] for t in tracks_data) / count,
        'instrumental': sum(t[12] for t in tracks_data) / count,
        'valence': sum(t[13] for t in tracks_data) / count,
    }

# Sorter / Cache Creator
def create_playlist_json(uri):
    client = SpotifyClient.get_instance()
    tracks = client.get_playlist_tracks(uri)
    
    track_ids = []
    track_items = []
    
    for item in tracks:
        # Filter out local files or invalid tracks that have no ID
        if not item['track'] or not item['track'].get('id'): 
            continue
        track_ids.append(item['track']['id'])
        track_items.append(item['track'])
        
    # Batch get audio features
    all_features = client.get_audio_features_batch(track_ids)
    
    track_metadata = {}
    
    for track, features in zip(track_items, all_features):
        if not features: 
            reason = "No audio features found"
            if track.get('is_local'):
                reason = "Track is local file"
            elif not track.get('id'):
                reason = "Track has no ID"
            
            print(f"Warning: Track {track['name']} (ID: {track.get('id')}) - {reason}. Using default values.")
            # Create default features with 0/None values so the track is still listed
            features = {
                'danceability': 0, 'energy': 0, 'acousticness': 0, 
                'instrumentalness': 0, 'valence': 0, 'liveness': 0, 
                'tempo': 0, 'mode': 0
            }
        
        track_uri = track['uri'].split(':')[2]
        
        track_metadata[track_uri] = {
            'nombre': track['name'],
            'n_disc': track['disc_number'],
            'n_track': track['track_number'],
            'album': track['album']['name'],
            'ano': track['album']['release_date'][:4] if track['album']['release_date'] else "0000",
            'mes': track['album']['release_date'][5:7] if len(track['album']['release_date']) > 5 else "01",
            'dia': track['album']['release_date'][8:10] if len(track['album']['release_date']) > 8 else "01",
            'artistas': [a['name'] for a in track['artists']],
            'id': track['id'],
            'danceability': features.get('danceability', 0),
            'energy': features.get('energy', 0),
            'acousticness': features.get('acousticness', 0),
            'instrumentalness': features.get('instrumentalness', 0),
            'valence': features.get('valence', 0),
            'liveness': features.get('liveness', 0),
            'tempo': features.get('tempo', 0),
            'mode': features.get('mode', 0)
        }

    add_tracks_to_playlist(uri, track_metadata)

# JSON load playlists
def load_master_file(master_file_path=f'{CACHE_DIR}/playlists.json'):
    if os.path.exists(master_file_path):
        with open(master_file_path, 'r', encoding='utf-8') as master_file:
            return json.load(master_file)
    return None

# JSON access playlist file
def get_playlist_track_file(playlist_uri, master_file_path=f'{CACHE_DIR}/playlists.json'):
    playlists = load_master_file(master_file_path)
    if playlists and playlist_uri in playlists:
        return playlists[playlist_uri]['tracks_file']
    return None

# JSON add tracks to playlist
def add_tracks_to_playlist(playlist_uri, track_metadata, master_file_path=f'{CACHE_DIR}/playlists.json'):
    if not os.path.exists(master_file_path):
        return
    
    with open(master_file_path, 'r', encoding='utf-8') as master_file:
        playlists = json.load(master_file)

    if playlist_uri not in playlists:
        return
    
    playlist_file_path = playlists[playlist_uri]['tracks_file']
    os.makedirs(os.path.dirname(playlist_file_path), exist_ok=True)

    existing_tracks = {}
    if os.path.exists(playlist_file_path):
        with open(playlist_file_path, 'r', encoding='utf-8') as playlist_file:
            existing_tracks = json.load(playlist_file)

    existing_tracks.update(track_metadata)

    with open(playlist_file_path, 'w', encoding='utf-8') as playlist_file:
        json.dump(existing_tracks, playlist_file, ensure_ascii=False, indent=4)
    
    print(f"Tracks added to {playlists[playlist_uri]['name']}.")
