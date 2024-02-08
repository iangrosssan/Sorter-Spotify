import spotipy
import spotipy.util as util

with open("credenciales.csv", "r") as archivo:
    linea = archivo.readlines()
    cid = linea[0].split(',')[0]
    secret = linea[0].split(',')[1]
redirect_uri = 'http://localhost:8888/callback'
scope = 'playlist-modify-public playlist-modify-private'

token = util.prompt_for_user_token(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scope)
sp2 = spotipy.Spotify(auth=token)


def obtener_playlists():
    playlists = []
    for i in sp2.user_playlists('22qojolff2pzjzcko4uvzu2ia')['items']:
        playlists.append(f"{i['name']}:{i['id']}")
    return playlists


def obtener_tracks(uri):
    results = sp2.user_playlist_tracks('22qojolff2pzjzcko4uvzu2ia',playlist_id=uri)
    tracks = results['items']
    while results['next']:
        results = sp2.next(results)
        tracks.extend(results['items'])
    return tracks


def ordenar_playlist(uri):
    ordenadas = []
    open('d_uri.csv', 'w').close()
    open('o_uri.csv', 'w').close()
    for i in obtener_tracks(uri):
        info_cancion = []
        nombre = i['track']['name']
        info_cancion.append(nombre)
        n_disc = i['track']['disc_number']
        info_cancion.append(n_disc)
        n_track = i['track']['track_number']
        info_cancion.append(n_track)
        album = i['track']['album']['name']
        info_cancion.append(album)
        ano = i['track']['album']['release_date'][:4]
        info_cancion.append(ano)
        mes = i['track']['album']['release_date'][5:7]
        info_cancion.append(mes)
        dia = i['track']['album']['release_date'][8:10]
        info_cancion.append(dia)
        artistas = []
        for j in i['track']['artists']:
            artistas.append(j['name'])
        info_cancion.append(artistas)
        track_uri = i['track']['uri'].split(':')[2]
        info_cancion.append(track_uri)
        ordenadas.append(info_cancion)
        with open('d_uri.csv', 'a') as d_uri:
            d_uri.write(f"{track_uri};")
    ordenadas.sort(key=lambda x: (x[7][0], x[4], x[5], x[6], x[1], x[2]))
    for i in ordenadas:
        with open('o_uri.csv','a') as o_uri:
            o_uri.write(f"{i[8]};")
    return ordenadas


def ordenar_en_app(uri):
    ordenadas = open('o_uri.csv', 'r')
    o_uri = ordenadas.readline().split(';')[:-1]
    ordenadas.close()
    desordenadas = open('d_uri.csv','r+')
    d_uri = desordenadas.readline().split(';')[:-1]
    n = 0
    for n_uri in o_uri:
        sp2.user_playlist_reorder_tracks('22qojolff2pzjzcko4uvzu2ia',playlist_id=uri,range_start=d_uri.index(n_uri), insert_before=n)
        cambio = d_uri.pop(d_uri.index(n_uri))
        d_uri.insert(0, cambio)
        n += 1
        print(f"{n}/{len(o_uri)}")


# def ordenar_en_app(uri):
#     ordenadas = open('o_uri.csv', 'r')
#     o_uri = ordenadas.readline().split(';')[:-1]
#     print(o_uri)
#     ordenadas.close()
#     desordenadas = open('d_uri.csv','r+')
#     d_uri = desordenadas.readline().split(';')[:-1]
#     ultima = len(o_uri)
#     for i in range(len(o_uri)):
#         print(i, d_uri)
#         while d_uri[i] != o_uri[i]:
#             sp2.user_playlist_reorder_tracks('22qojolff2pzjzcko4uvzu2ia',playlist_id=uri,range_start=i, insert_before=ultima)
#             cambio = d_uri.pop(i)
#             print("pop", cambio)
#             d_uri += [cambio]
#     print("finalizado")
