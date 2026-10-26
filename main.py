import sys
from PySide6.QtWidgets import QApplication
from src.gui_v2 import LanzadorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    ventana = LanzadorApp()
    ventana.show()
    sys.exit(app.exec())

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = LanzadorApp(root)
#     root.mainloop()