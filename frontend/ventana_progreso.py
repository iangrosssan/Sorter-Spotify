import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUiType

window_name, base_class = loadUiType("frontend/ventana_progreso.ui")


class VentanaProgreso(window_name, base_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def actualizar_label(self,n,n_total):
        self.label.setText(f"{n} de {n_total}")


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaProgreso()
    ventana.show()
    sys.exit(app.exec_())
