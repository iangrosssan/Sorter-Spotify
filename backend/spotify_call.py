import spotipy
import spotipy.util as util

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


# Spotify call playlists
def obtener_playlists():
    playlists = []
    for i in sp2.user_playlists(user)['items']:
        playlists.append(f"{i['name']}:{i['id']}")
    return playlists


# Spotify call tracks
def obtener_tracks(uri):
    results = sp2.user_playlist_tracks(user,playlist_id=uri)
    tracks = results['items']
    while results['next']:
        results = sp2.next(results)
        tracks.extend(results['items'])
    return tracks


def get_metadata(track_id):
    metadata = sp2.audio_features(track_id)[0]
    danceability = metadata['danceability']
    energy = metadata['energy']
    speechiness = metadata['speechiness']
    acousticness = metadata['acousticness']
    instrumentalness = metadata['instrumentalness']
    valence = metadata['valence']
    liveness = metadata['liveness'] # Flag live tracks
    tempo = metadata['tempo'] # Custom Order
    mode = metadata['mode'] # Custom Order
    return danceability, energy, speechiness, acousticness, instrumentalness, valence, liveness, tempo, mode


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
    desordenadas.close()
