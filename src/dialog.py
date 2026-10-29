from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QHBoxLayout, QLabel,
    QLineEdit, QMessageBox, QPushButton, QVBoxLayout,
)
from src.config_manager import guardar_nueva_app, editar_app


class ConfigDialog(QDialog):
    """Ventana flotante para añadir o editar una aplicación en el perfil actual"""

    def __init__(self, parent=None, perfil_actual="Desarrollo", nombre_inicial="", comando_inicial=""):
        super().__init__(parent)
        self.perfil_actual = perfil_actual
        self.es_edicion = bool(nombre_inicial)
        self.nombre_antiguo = nombre_inicial

        titulo = f"Editar en [{perfil_actual}]" if self.es_edicion else f"Añadir a [{perfil_actual}]"
        self.setWindowTitle(titulo)
        self.setFixedSize(380, 220)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Nombre de la app
        layout.addWidget(QLabel("Nombre de la aplicación:"))
        self.input_nombre = QLineEdit(self)
        self.input_nombre.setText(nombre_inicial)
        self.input_nombre.setPlaceholderText("Ej: Postman, Notion...")
        layout.addWidget(self.input_nombre)

        # Ruta o comando
        layout.addWidget(QLabel("Ruta del ejecutable o comando:"))
        layout_ruta = QHBoxLayout()
        self.input_ruta = QLineEdit(self)
        self.input_ruta.setText(comando_inicial)
        self.input_ruta.setPlaceholderText("Ej: code o C:\\Ruta\\app.exe")
        layout_ruta.addWidget(self.input_ruta)

        btn_examinar = QPushButton("...", self)
        btn_examinar.setFixedWidth(40)
        btn_examinar.clicked.connect(self.explorar_archivo)
        layout_ruta.addWidget(btn_examinar)
        layout.addLayout(layout_ruta)

        # Botones Guardar / Cancelar
        layout_botones = QHBoxLayout()
        btn_guardar = QPushButton("Guardar", self)
        btn_guardar.setStyleSheet(
            "background-color: #0078D4; color: white; font-weight: bold; padding: 6px;"
        )
        btn_guardar.clicked.connect(self.validar_y_guardar)

        btn_cancelar = QPushButton("Cancelar", self)
        btn_cancelar.clicked.connect(self.reject)

        layout_botones.addWidget(btn_cancelar)
        layout_botones.addWidget(btn_guardar)
        layout.addLayout(layout_botones)

    def explorar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Ejecutable", "", "Ejecutables (*.exe);;Todos (*.*)"
        )
        if archivo:
            self.input_ruta.setText(archivo)

    def validar_y_guardar(self):
        nombre = self.input_nombre.text().strip()
        comando = self.input_ruta.text().strip()

        if not nombre or not comando:
            QMessageBox.warning(
                self, "Aviso", "Rellena todos los campos obligatorios."
            )
            return

        if self.es_edicion:
            editar_app(self.perfil_actual, self.nombre_antiguo, nombre, comando)
        else:
            guardar_nueva_app(self.perfil_actual, nombre, comando)

        self.accept()