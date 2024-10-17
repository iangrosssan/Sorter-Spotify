import sys
import os, json

from backend.funciones import get_track_data, average_metadata
from backend.sorters import sort_tracks
from backend.spotify_call import ordenar_en_app
from backend.classes import StatsPolygon

from PyQt5.QtWidgets import QApplication, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUiType

window_name, base_class = loadUiType("frontend/ventana_ordenadas3.ui")


class VentanaOrdenadas(window_name, base_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.uri = ""
        self.data_file = None
        self.metadata = []
        self.jerarquias.verticalScrollBar().setCursor(Qt.OpenHandCursor)
        self.jerarquias.verticalScrollBar().sliderPressed.connect(self.on_slider_pressed)
        self.jerarquias.verticalScrollBar().sliderReleased.connect(self.on_slider_released)
        self.lista_playlists.verticalScrollBar().setCursor(Qt.OpenHandCursor)
        self.lista_playlists.verticalScrollBar().sliderPressed.connect(self.on_slider_pressed)
        self.lista_playlists.verticalScrollBar().sliderReleased.connect(self.on_slider_released)


    def clear(self):
        self.progressBar.setValue(0)
        self.jerarquias.selectRow(0)


    def print_list(self):
        self.lista_playlists.clear()
        artista = ''
        album = ''
        tracks_data = get_track_data(self.uri)
        self.stats = average_metadata(tracks_data)
        tracks_data = sort_tracks(tracks_data, self.jerarquias.selectedIndexes()[0].row())
        for track in tracks_data:
            if artista == '':
                artista = track[8][0]
                item = QTreeWidgetItem(self.lista_playlists)
                item.setText(0, f'{artista}')
            elif artista != track[8][0]:
                artista = track[8][0]
                item = QTreeWidgetItem(self.lista_playlists)
                item.setText(0, f"\n\n{artista}")
                album = ''
            if album == '':
                album = track[4]
                item_child = QTreeWidgetItem(self.lista_playlists)
                item_child.setText(0, f"   {album}")
                item.addChild(item_child)
            elif album != track[4]:
                album = track[4]
                item_child = QTreeWidgetItem(self.lista_playlists)
                item_child.setText(0, f"\n   {album}")
                item.addChild(item_child)
            item_grandchild = QTreeWidgetItem(self.lista_playlists)
            item_grandchild.setText(0, f"\t{track[1]}")
            tooltip = f'''<b>Dance:</b> {track[9]}<br>
                        <b>Energy:</b> {track[10]}<br>
                        <b>Lyrical:</b> {track[11]}<br>
                        <b>Acoustic:</b> {track[12]}<br>
                        <b>Instrumental:</b> {track[13]}<br>
                        <b>Valence:</b> {track[14]}<br>
                        <b>Live:</b> {track[15]}'''
            item_grandchild.setToolTip(0, tooltip)
            item_child.addChild(item_grandchild)
        StatsPolygon(self.l_stats, self.stats)

    def ordenar(self):
        for i in ordenar_en_app(self.uri):
            actual = int(i.split("/")[0])
            if actual == 1:
                total = int(i.split("/")[1])
                self.progressBar.setMaximum(total)
            self.progressBar.setValue(actual)


    def on_slider_pressed(self):
        self.sender().setCursor(Qt.ClosedHandCursor)
    

    def on_slider_released(self):
        self.sender().setCursor(Qt.OpenHandCursor)


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaOrdenadas()
    ventana.show()
    sys.exit(app.exec_())
