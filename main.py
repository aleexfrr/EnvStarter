import sys
from PyQt6.QtWidgets import QApplication
from src.gui import LanzadorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ventana = LanzadorApp()
    ventana.show()
    sys.exit(app.exec())