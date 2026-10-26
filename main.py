import sys
from PySide6.QtWidgets import QApplication
from src.gui import LanzadorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    ventana = LanzadorApp()
    ventana.show()
    sys.exit(app.exec())