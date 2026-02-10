import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ordenadas import VentanaOrdenadas

from backend.funciones import get_playlist_track_file, guardar_playlists
from backend.spotify_call import SpotifyClient
    

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    with open("frontend/styles.qss", "r") as file:
        stylesheet = file.read()
        app.setStyleSheet(stylesheet)


# FUNCIONES
def abrir_ordenadas(indice):
    client = SpotifyClient.get_instance()
    playlists = client.get_user_playlists()
    guardar_playlists(playlists)
    ventana_ordenadas.l_nombre.setText(playlists[indice].split(":")[0])
    ventana_ordenadas.uri = playlists[indice].split(":")[1].strip()
    ventana_ordenadas.data_file = get_playlist_track_file(ventana_ordenadas.uri)
    if not ventana_ordenadas.isVisible():
        ventana_ordenadas.show()
    ventana_ordenadas.print_list()


# INSTANCIAS
ventana_inicio = VentanaInicio()
ventana_ordenadas = VentanaOrdenadas()


# FLUJO
ventana_inicio.actualizar()
ventana_inicio.show()

ventana_inicio.t_playlists.clicked.connect(ventana_inicio.activar_botones)

ventana_inicio.b_ordenar.clicked.connect(ventana_ordenadas.clear)
ventana_inicio.b_ordenar.clicked.connect(lambda: abrir_ordenadas(ventana_inicio.seleccion()))

ventana_ordenadas.b_ordenar.clicked.connect(lambda: ventana_ordenadas.ordenar())
ventana_ordenadas.jerarquias.clicked.connect(lambda: ventana_ordenadas.print_list())
ventana_ordenadas.jerarquias.clicked.connect(lambda: ventana_ordenadas.progressBar.setValue(0))


app.exec_()
