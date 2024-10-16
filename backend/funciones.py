import spotipy
import spotipy.util as util
import os, json

from backend.classes import PlaylistMetaData
from backend.sorters import shuffle_with_groups, simple_shuffle, jerarquias


# Credenciales
with open("backend/credenciales.csv", "r") as archivo:
    linea = archivo.readlines()
    cid = linea[0].split(',')[0]
    secret = linea[0].split(',')[1]
    user = linea[0].split(',')[2].strip()
redirect_uri = 'http://localhost:8888/callback'
scope = 'playlist-modify-public playlist-modify-private'

token = util.prompt_for_user_token(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope)
sp2 = spotipy.Spotify(auth=token)


# Stylesheet
def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()


# Spotify call playlists
def obtener_playlists():
    playlists = []
    for i in sp2.user_playlists(user)['items']:
        playlists.append(f"{i['name']}:{i['id']}")
    guardar_playlists(playlists)
    return playlists


# JSON playlists
def guardar_playlists(playlists):
    playlists = {
        uri: {'name': name, 'tracks_file': f'backend/attribute_cache/{uri}.json'} for name, uri in [i.split(':') for i in playlists]
    }
    with open('backend/attribute_cache/playlists.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(playlists, jsonfile, ensure_ascii=False, indent=4)


# Spotify call tracks
def obtener_tracks(uri):
    results = sp2.user_playlist_tracks(user,playlist_id=uri)
    tracks = results['items']
    while results['next']:
        results = sp2.next(results)
        tracks.extend(results['items'])
    return tracks


def get_track_data(uri, jerarquia):
    playlist_file_path = get_playlist_track_file(uri)
    if not os.path.isfile(playlist_file_path):
        ordenar_playlist(uri, jerarquia)

    with open(playlist_file_path, 'r', encoding='utf-8') as playlist_file:
        track_metadata = json.load(playlist_file)

    tracks = obtener_tracks(uri)
    tracks_uri = [track['track']['uri'].split(':')[2] for track in tracks]

    l_tracks = []
    for uri in tracks_uri:
        if uri not in track_metadata:
            continue
        info_track = []
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
        

# Sorter
def ordenar_playlist(uri, jerarquia):
    ordenadas = []
    metadata_old = []
    playlist_metadata = PlaylistMetaData()

    open('backend/d_uri.csv', 'w').close()
    open('backend/o_uri.csv', 'w').close()

    for i in obtener_tracks(uri):
        track_uri = i['track']['uri'].split(':')[2]
        with open('backend/d_uri.csv', 'a') as d_uri:
            d_uri.write(f"{track_uri};")

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
        danceability = sp2.audio_features(track_id)[0]['danceability']
        energy = sp2.audio_features(track_id)[0]['energy']
        speechiness = sp2.audio_features(track_id)[0]['speechiness']
        acousticness = sp2.audio_features(track_id)[0]['acousticness']
        instrumentalness = sp2.audio_features(track_id)[0]['instrumentalness']
        valence = sp2.audio_features(track_id)[0]['valence']
        liveness = sp2.audio_features(track_id)[0]['liveness'] # Flag live tracks
        tempo = sp2.audio_features(track_id)[0]['tempo'] # Custom Order
        mode = sp2.audio_features(track_id)[0]['mode'] # Custom Order
        
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
        

        track_metadata_old = [danceability, energy, speechiness, acousticness, instrumentalness, valence, liveness, tempo, mode]
        metadata_old.append(track_metadata_old)
        playlist_metadata.add_track(track_metadata_old)


    if jerarquia == 1:
        ordenadas = shuffle_with_groups(ordenadas)
    elif jerarquia == 3:
        ordenadas = simple_shuffle(ordenadas)
    else:
        key = jerarquias[jerarquia]
        ordenadas.sort(key=key)
    #ordenadas.sort(key=lambda x: (x[7][0], x[4], x[5], x[6], x[1], x[2]))
                                # Artista, año,  mes,  dia, disco, track
    for i in ordenadas:
        with open('backend/o_uri.csv', 'a') as o_uri:
            o_uri.write(f"{i[8]};")
    return ordenadas, metadata_old, playlist_metadata.get_average_features()


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



def ordenar_en_app(uri):
    ordenadas = open('backend/o_uri.csv', 'r')
    o_uri = ordenadas.readline().split(';')[:-1]
    ordenadas.close()
    desordenadas = open('backend/d_uri.csv', 'r+')
    d_uri = desordenadas.readline().split(';')[:-1]
    n = 0
    for n_uri in o_uri:
        sp2.user_playlist_reorder_tracks(user,playlist_id=uri,range_start=d_uri.index(n_uri), insert_before=n)
        cambio = d_uri.pop(d_uri.index(n_uri))
        d_uri.insert(0, cambio)
        n += 1
        yield f"{n}/{len(o_uri)}"
