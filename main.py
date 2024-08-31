import sys

from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ordenadas import VentanaOrdenadas
from frontend.ventana_progreso import VentanaProgreso


if __name__ == '__main__':
    def hook(type, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])


# INSTANCIAS
ventana_inicio = VentanaInicio()
ventana_ordenadas = VentanaOrdenadas()
ventana_progreso = VentanaProgreso()


# FUNCIONES
def abrir_ordenadas():
    if not ventana_ordenadas.isVisible():
        ventana_ordenadas.show()
    else:
        ventana_ordenadas.hide()


def abrir_progreso():
    if not ventana_progreso.isVisible():
        ventana_progreso.show()
    else:
        ventana_progreso.hide()


# FLUJO
ventana_inicio.actualizar()
ventana_inicio.show()

ventana_inicio.t_playlists.clicked.connect(ventana_inicio.activar_botones)

ventana_inicio.b_ordenar.clicked.connect(ventana_ordenadas.clear)
ventana_inicio.b_ordenar.clicked.connect(lambda: ventana_ordenadas.playlist_elegida(ventana_inicio.seleccion()))
ventana_inicio.b_ordenar.clicked.connect(abrir_ordenadas)

#ventana_ordenadas.b_ordenar.clicked.connect(abrir_progreso)
ventana_ordenadas.b_ordenar.clicked.connect(lambda: ventana_ordenadas.ordenar())


app.exec_()
