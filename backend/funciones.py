import os, json

from backend.spotify_call import obtener_tracks, get_metadata


# JSON playlists
def guardar_playlists(playlists):
    playlists = {
        uri: {'name': name, 'tracks_file': f'backend/attribute_cache/{uri}.json'} for name, uri in [i.split(':') for i in playlists]
    }
    with open('backend/attribute_cache/playlists.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(playlists, jsonfile, ensure_ascii=False, indent=4)


def get_track_data(uri):
    playlist_file_path = get_playlist_track_file(uri)
    if not os.path.isfile(playlist_file_path):
        create_playlist_json(uri)

    with open(playlist_file_path, 'r', encoding='utf-8') as playlist_file:
        track_metadata = json.load(playlist_file)

    tracks = obtener_tracks(uri)
    tracks_uri = [track['track']['uri'].split(':')[2] for track in tracks]

    l_tracks = []
    for uri in tracks_uri:
        if uri not in track_metadata:
            continue
        info_track = []
        info_track.append(uri)
        track_name = track_metadata[f'{uri}']['nombre']
        info_track.append(track_name)
        track_disc = track_metadata[f'{uri}']['n_disc']
        info_track.append(track_disc)
        track_number = track_metadata[f'{uri}']['n_track']
        info_track.append(track_number)
        track_album = track_metadata[f'{uri}']['album']
        info_track.append(track_album)
        track_year = track_metadata[f'{uri}']['ano']
        info_track.append(track_year)
        track_month = track_metadata[f'{uri}']['mes']
        info_track.append(track_month)
        track_day = track_metadata[f'{uri}']['dia']
        info_track.append(track_day)
        track_artists = track_metadata[f'{uri}']['artistas']
        info_track.append(track_artists)
        danceability = track_metadata[f'{uri}']['danceability']
        info_track.append(danceability)
        energy = track_metadata[f'{uri}']['energy']
        info_track.append(energy)
        speechiness = track_metadata[f'{uri}']['speechiness']
        info_track.append(speechiness)
        acousticness = track_metadata[f'{uri}']['acousticness']
        info_track.append(acousticness)
        instrumentalness = track_metadata[f'{uri}']['instrumentalness']
        info_track.append(instrumentalness)
        valence = track_metadata[f'{uri}']['valence']
        info_track.append(valence)
        liveness = track_metadata[f'{uri}']['liveness']
        info_track.append(liveness)
        tempo = track_metadata[f'{uri}']['tempo']
        info_track.append(tempo)
        mode = track_metadata[f'{uri}']['mode']
        info_track.append(mode)
        l_tracks.append(info_track)
    return l_tracks


def average_metadata(tracks_data):
    danceability = sum([track[9] for track in tracks_data]) / len(tracks_data)
    energy = sum([track[10] for track in tracks_data]) / len(tracks_data)
    speechiness = sum([track[11] for track in tracks_data]) / len(tracks_data)
    acousticness = sum([track[12] for track in tracks_data]) / len(tracks_data)
    instrumentalness = sum([track[13] for track in tracks_data]) / len(tracks_data)
    valence = sum([track[14] for track in tracks_data]) / len(tracks_data)
    dict_stats = {
        'dance': danceability,
        'energy': energy,
        'lyrical': speechiness,
        'acoustic': acousticness,
        'instrumental': instrumentalness,
        'valence': valence,
    }
    return dict_stats



# Sorter
def create_playlist_json(uri):
    for i in obtener_tracks(uri):
        track_uri = i['track']['uri'].split(':')[2]

        # Playlist Metadata Info
        nombre = i['track']['name']
        n_disc = i['track']['disc_number']
        n_track = i['track']['track_number']
        album = i['track']['album']['name']
        ano = i['track']['album']['release_date'][:4]
        mes = i['track']['album']['release_date'][5:7]
        dia = i['track']['album']['release_date'][8:10]
        artistas = []
        for j in i['track']['artists']:
            artista = j['name']
            artistas.append(artista)

        track_id = i['track']['id']
        danceability, energy, speechiness, acousticness, instrumentalness,valence, liveness, tempo, mode = get_metadata(track_id)

        
        track_metadata = {
            track_uri: {
                'nombre': nombre,
                'n_disc': n_disc,
                'n_track': n_track,
                'album': album,
                'ano': ano,
                'mes': mes,
                'dia': dia,
                'artistas': artistas,
                'id': track_id,
                'danceability': danceability,
                'energy': energy,
                'speechiness': speechiness,
                'acousticness': acousticness,
                'instrumentalness': instrumentalness,
                'valence': valence,
                'liveness': liveness,
                'tempo': tempo,
                'mode': mode
            }
        }

        add_tracks_to_playlist(uri, track_metadata)



# JSON load playlists
def load_master_file(master_file_path='backend/attribute_cache/playlists.json'):
    if os.path.exists(master_file_path):
        with open(master_file_path, 'r', encoding='utf-8') as master_file:
            playlists = json.load(master_file)
            return playlists
    else:
        return None


# JSON access playlist file
def get_playlist_track_file(playlist_uri, master_file_path='backend/attribute_cache/playlists.json'):
    playlists = load_master_file(master_file_path)
    
    if playlists is None:
        return None
    
    # Check if the playlist exists in the master file
    if playlist_uri in playlists:
        playlist_file_path = playlists[playlist_uri]['tracks_file']
        return playlist_file_path


# JSON add tracks to playlist
def add_tracks_to_playlist(playlist_uri, track_metadata, master_file_path='backend/attribute_cache/playlists.json'):
    # Load the master JSON file
    if not os.path.exists(master_file_path):
        print(f"Master file {master_file_path} does not exist.")
        return
    
    with open(master_file_path, 'r', encoding='utf-8') as master_file:
        playlists = json.load(master_file)

    # Check if the playlist exists in the master file
    if playlist_uri not in playlists:
        print(f"Playlist {playlist_uri} not found.")
        return
    
    # Get the track file path from the master JSON
    playlist_file_path = playlists[playlist_uri]['tracks_file']

    # Load existing track metadata from the track file (or start fresh)
    if os.path.exists(playlist_file_path):
        with open(playlist_file_path, 'r', encoding='utf-8') as playlist_file:
            existing_tracks = json.load(playlist_file)
    else:
        existing_tracks = {}

    # Add or update the track metadata
    existing_tracks.update(track_metadata)

    # Save the updated tracks back to the track file
    with open(playlist_file_path, 'w', encoding='utf-8') as playlist_file:
        json.dump(existing_tracks, playlist_file, ensure_ascii=False, indent=4)
    
    print(f"Tracks added to {playlists[playlist_uri]['name']}.")
