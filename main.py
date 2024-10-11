import sys

from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ordenadas import VentanaOrdenadas

from backend.funciones import PlaylistMetaData


#FUNCIONES
def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()
    

def abrir_ordenadas():
    if not ventana_ordenadas.isVisible():
        ventana_ordenadas.show()
#         load_metadata()


# def load_metadata():
#     playlist_metadata = PlaylistMetaData()
    

    

if __name__ == '__main__':
    def hook(type, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    stylesheet = load_stylesheet("frontend/styles.qss")
    app.setStyleSheet(stylesheet)



# INSTANCIAS
ventana_inicio = VentanaInicio()
ventana_ordenadas = VentanaOrdenadas()


# FLUJO
ventana_inicio.actualizar()
ventana_inicio.show()

ventana_inicio.t_playlists.clicked.connect(ventana_inicio.activar_botones)

ventana_inicio.b_ordenar.clicked.connect(ventana_ordenadas.clear)
ventana_inicio.b_ordenar.clicked.connect(lambda: ventana_ordenadas.playlist_elegida(ventana_inicio.seleccion()))
ventana_inicio.b_ordenar.clicked.connect(abrir_ordenadas)

ventana_ordenadas.b_ordenar.clicked.connect(lambda: ventana_ordenadas.ordenar())
ventana_ordenadas.jerarquias.clicked.connect(lambda: ventana_ordenadas.print_list())
ventana_ordenadas.jerarquias.clicked.connect(lambda: ventana_ordenadas.progressBar.setValue(0))


app.exec_()
