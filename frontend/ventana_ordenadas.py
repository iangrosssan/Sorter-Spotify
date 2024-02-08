import sys

from frontend.funciones import obtener_playlists, ordenar_playlist, ordenar_en_app

from PyQt5.QtWidgets import QApplication, QTreeWidgetItem
from PyQt5.uic import loadUiType

window_name, base_class = loadUiType("frontend/ventana_ordenadas2.ui")


class VentanaOrdenadas(window_name, base_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.uri = ""

    def playlist_elegida(self, indice):
        playlists = obtener_playlists()
        self.l_nombre.setText(playlists[indice].split(":")[0])
        self.uri = playlists[indice].split(":")[1].strip()
        self.print_list()

    def print_list(self):
        self.lista_playlists.clear()
        artista = ''
        album = ''
        tracks = ordenar_playlist(self.uri)
        for track in tracks:
            if artista == '':
                artista = track[7][0]
                item = QTreeWidgetItem(self.lista_playlists)
                item.setText(0, artista)
            elif artista != track[7][0]:
                artista = track[7][0]
                item = QTreeWidgetItem(self.lista_playlists)
                item.setText(0, f"\n\n{artista}")
                album = ''
            if album == '':
                album = track[3]
                item_child = QTreeWidgetItem(self.lista_playlists)
                item_child.setText(0, f"   {album}")
                item.addChild(item_child)
            elif album != track[3]:
                album = track[3]
                item_child = QTreeWidgetItem(self.lista_playlists)
                item_child.setText(0, f"\n   {album}")
                item.addChild(item_child)
            item_grandchild = QTreeWidgetItem(self.lista_playlists)
            item_grandchild.setText(0, f"\t{track[0]}")
            item_child.addChild(item_grandchild)

    def ordenar_en_app(self):
        ordenar_en_app(self.uri)


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaOrdenadas()
    ventana.show()
    sys.exit(app.exec_())
