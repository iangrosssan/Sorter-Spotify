import spotipy
import spotipy.util as util
import random
from itertools import groupby

from backend.classes import PlaylistMetaData


with open("backend/credenciales.csv", "r") as archivo:
    linea = archivo.readlines()
    cid = linea[0].split(',')[0]
    secret = linea[0].split(',')[1]
    user = linea[0].split(',')[2].strip()
redirect_uri = 'http://localhost:8888/callback'
scope = 'playlist-modify-public playlist-modify-private'

token = util.prompt_for_user_token(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope)
sp2 = spotipy.Spotify(auth=token)


def obtener_playlists():
    playlists = []
    for i in sp2.user_playlists(user)['items']:
        playlists.append(f"{i['name']}:{i['id']}")
    return playlists


def obtener_tracks(uri):
    results = sp2.user_playlist_tracks(user,playlist_id=uri)
    tracks = results['items']
    while results['next']:
        results = sp2.next(results)
        tracks.extend(results['items'])
    return tracks


def ordenar_playlist(uri, jerarquia):
    ordenadas = []
    metadata = []
    playlist_metadata = PlaylistMetaData()
    open('backend/d_uri.csv', 'w').close()
    open('backend/o_uri.csv', 'w').close()
    for i in obtener_tracks(uri):
        info_cancion = []

        nombre = i['track']['name']
        info_cancion.append(nombre) #0
                
        n_disc = i['track']['disc_number']
        info_cancion.append(n_disc) #1
        
        n_track = i['track']['track_number']
        info_cancion.append(n_track) #2
        
        album = i['track']['album']['name']
        info_cancion.append(album) #3
        
        ano = i['track']['album']['release_date'][:4]
        info_cancion.append(ano) #4
        
        mes = i['track']['album']['release_date'][5:7]
        info_cancion.append(mes) #5
        
        dia = i['track']['album']['release_date'][8:10]
        info_cancion.append(dia) #6
        
        artistas = []
        for j in i['track']['artists']:
            artistas.append(j['name'])
        info_cancion.append(artistas) #7
        
        track_uri = i['track']['uri'].split(':')[2]
        info_cancion.append(track_uri)
        ordenadas.append(info_cancion)
        with open('backend/d_uri.csv', 'a') as d_uri:
            d_uri.write(f"{track_uri};")
        
        # Playlist Metadata Info
        track_id = i['track']['id']

        # danceability = sp2.audio_features(track_id)[0]['danceability']
        # energy = sp2.audio_features(track_id)[0]['energy']
        # speechiness = sp2.audio_features(track_id)[0]['speechiness']
        # acousticness = sp2.audio_features(track_id)[0]['acousticness']
        # instrumentalness = sp2.audio_features(track_id)[0]['instrumentalness']
        # valence = sp2.audio_features(track_id)[0]['valence']
        # liveness = sp2.audio_features(track_id)[0]['liveness'] # Flag live tracks
        # tempo = sp2.audio_features(track_id)[0]['tempo'] # Custom Order
        # mode = sp2.audio_features(track_id)[0]['mode'] # Custom Order
        danceability = 0.5
        energy = 0.9
        speechiness = 0.1
        acousticness = 0.6
        instrumentalness = 0.7
        valence = 0.3
        liveness = 0.5
        tempo = 0.5
        mode = 0.5
        track_metadata = [danceability, energy, speechiness, acousticness, instrumentalness, valence, liveness, tempo, mode]
        metadata.append(track_metadata)
        playlist_metadata.add_track(track_metadata)

    #print(jerarquias[jerarquia].strip())
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
    return ordenadas, metadata, playlist_metadata.get_average_features()


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


def shuffle_with_groups(ordenadas):
    # Step 1: Sort the list to group identical items together
    sorted_list = sorted(ordenadas, key=lambda x: (x[7][0], x[4], x[5], x[6], x[1], x[2]))
    
    # Step 2: Group the identical items together
    groups = [list(group) for key, group in groupby(sorted_list, key=lambda x: x[7][0])]
    
    # Step 3: Shuffle the groups themselves
    random.shuffle(groups)
    
    # Step 4: Flatten the list of groups
    shuffled_list = [item for group in groups for item in group]
    
    return shuffled_list


def simple_shuffle(ordenadas):
    random.shuffle(ordenadas)
    return ordenadas


jerarquias = [lambda x: (x[7][0], x[4], x[5], x[6], x[1], x[2]), None,
              lambda x: (x[4], x[5], x[6], x[1], x[2]),
              None]