import sys
import os, json

from backend.funciones import get_track_data, average_metadata
from backend.sorters import sort_tracks
from backend.spotify_call import SpotifyClient
from frontend.components import StatsPolygon

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
        self.sorted_data = [] # Store sorted data for access in ordenar()
        self.jerarquias.verticalScrollBar().setCursor(Qt.OpenHandCursor)
        self.jerarquias.verticalScrollBar().sliderPressed.connect(self.on_slider_pressed)
        self.jerarquias.verticalScrollBar().sliderReleased.connect(self.on_slider_released)
        self.lista_playlists.verticalScrollBar().setCursor(Qt.OpenHandCursor)
        self.lista_playlists.verticalScrollBar().sliderPressed.connect(self.on_slider_pressed)
        self.lista_playlists.verticalScrollBar().sliderReleased.connect(self.on_slider_released)

        from PyQt5.QtWidgets import QPushButton
        self.b_spotify = QPushButton(self)
        self.b_spotify.setText("Abrir en Spotify")
        self.b_spotify.setMinimumSize(200, 61)
        self.b_spotify.setMaximumSize(250, 61)
        self.b_spotify.setCursor(Qt.PointingHandCursor)
        self.horizontalLayout_4.addWidget(self.b_spotify)
        self.b_spotify.clicked.connect(self.abrir_en_spotify)


    def clear(self):
        self.progressBar.setValue(0)
        self.jerarquias.selectRow(0)


    def print_list(self):
        self.lista_playlists.clear()
        artista = ''
        album = ''
        tracks_data = get_track_data(self.uri)
        self.stats = average_metadata(tracks_data)
        
        # Sort and store
        self.sorted_data = sort_tracks(tracks_data, self.jerarquias.selectedIndexes()[0].row())
        
        for track in self.sorted_data:
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
        if not self.sorted_data:
            return

        client = SpotifyClient.get_instance()
        
        # We need the current URI list to know where to move things FROM
        # This fetching might take a moment, but it ensures accuracy
        current_tracks = client.get_playlist_tracks(self.uri)
        current_uris = [t['track']['uri'].split(':')[2] for t in current_tracks if t['track']]
        
        ordered_uris = [t[0] for t in self.sorted_data]
        
        # Generator yields progress strings like "1/100"
        for progress in client.reorder_playlist(self.uri, ordered_uris, current_uris):
            actual = int(progress.split("/")[0])
            if actual == 1:
                total = int(progress.split("/")[1])
                self.progressBar.setMaximum(total)
            self.progressBar.setValue(actual)

    def abrir_en_spotify(self):
        if self.uri:
            import webbrowser
            webbrowser.open(f"https://open.spotify.com/playlist/{self.uri}")



    def on_slider_pressed(self):
        self.sender().setCursor(Qt.ClosedHandCursor)
    

    def on_slider_released(self):
        self.sender().setCursor(Qt.OpenHandCursor)


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaOrdenadas()
    ventana.show()
    sys.exit(app.exec_())
