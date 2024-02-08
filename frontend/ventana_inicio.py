import sys

from backend.funciones import obtener_playlists

from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.uic import loadUiType

window_name, base_class = loadUiType("frontend/ventana_inicio.ui")


class VentanaInicio(window_name, base_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.b_ordenar.setEnabled(False)
        self.t_playlists.horizontalHeader().setFixedHeight(40)
        self.t_playlists.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)       
        self.t_playlists.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    
    def actualizar(self):
        playlists = obtener_playlists()
        self.t_playlists.setRowCount(len(playlists))
        for i in range(len(playlists)):
            self.t_playlists.setItem(i,0,QTableWidgetItem(playlists[i].split(":")[0]))
            self.t_playlists.setFont(QFont("Consolas", 12))
            self.t_playlists.setStyleSheet("background-color: white")
    
    def activar_botones(self):
        self.b_ordenar.setEnabled(True)

    def seleccion(self):
        i = self.t_playlists.selectedIndexes()[0].row()
        return i


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec_())
