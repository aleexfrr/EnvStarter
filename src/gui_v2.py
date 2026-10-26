import os
import subprocess
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from src.config import APPS


class LanzadorApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DevDeck - Panel de Control")
        self.setFixedSize(420, 500)

        # Cargar icono si existe en assets
        icon_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "icon.ico"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.vars_apps = {}
        self._crear_toolbar()
        self._crear_interfaz()

    def _crear_toolbar(self):
        toolbar = QToolBar("Barra Superior", self)
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        spacer = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        toolbar.addWidget(spacer)

        lbl_tema = QLabel("Tema: ", self)
        toolbar.addWidget(lbl_tema)

        self.combo_tema = QComboBox(self)
        self.combo_tema.addItems(["Oscuro", "Claro"])
        self.combo_tema.setCurrentText("Oscuro")
        self.combo_tema.currentTextChanged.connect(self.cambiar_tema)
        toolbar.addWidget(self.combo_tema)

        toolbar.setStyleSheet(
            "QToolBar { spacing: 6px; padding: 5px; background: transparent; border: none; }"
        )

    def _crear_interfaz(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout_principal = QVBoxLayout(central_widget)
        layout_principal.setContentsMargins(20, 10, 20, 20)
        layout_principal.setSpacing(12)

        # --- BLOQUE / GRUPO DE APLICACIONES ---
        group_box = QGroupBox("Aplicaciones del Entorno de Trabajo")
        layout_group = QVBoxLayout(group_box)
        layout_group.setSpacing(8)

        for app_name in APPS.keys():
            chk = QCheckBox(app_name, self)
            chk.setChecked(True)  # Por defecto marcadas
            layout_group.addWidget(chk)
            self.vars_apps[app_name] = chk

        layout_principal.addWidget(group_box)

        # --- BOTONES DE SELECCIÓN RÁPIDA ---
        layout_botones_sel = QHBoxLayout()
        self.btn_todos = QPushButton("Marcar todo", self)
        self.btn_todos.clicked.connect(self.seleccionar_todo)

        self.btn_ninguno = QPushButton("Desmarcar", self)
        self.btn_ninguno.clicked.connect(self.deseleccionar_todo)

        layout_botones_sel.addWidget(self.btn_todos)
        layout_botones_sel.addWidget(self.btn_ninguno)
        layout_principal.addLayout(layout_botones_sel)

        # --- BOTÓN PRINCIPAL DE LANZAMIENTO ---
        self.btn_lanzar = QPushButton("🚀 Lanzar Seleccionadas", self)
        self.btn_lanzar.setObjectName("btnLanzar")  # Asignamos ID para el estilo
        self.btn_lanzar.clicked.connect(self.lanzar_apps)
        layout_principal.addWidget(self.btn_lanzar)

    def seleccionar_todo(self):
        for chk in self.vars_apps.values():
            chk.setChecked(True)

    def deseleccionar_todo(self):
        for chk in self.vars_apps.values():
            chk.setChecked(False)

    def cambiar_tema(self, tema):
        app = QApplication.instance()

        if tema == "Oscuro":
            estilo_oscuro = """
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    font-family: 'Segoe UI';
                }
                QToolBar {
                    background: transparent;
                    border: none;
                }
                QLabel {
                    color: #ffffff;
                }
                QGroupBox {
                    font-family: 'Segoe UI';
                    font-size: 10pt;
                    font-weight: bold;
                    border: 1px solid #555555;
                    border-radius: 6px;
                    margin-top: 10px;
                    padding-top: 15px;
                    color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 5px;
                    color: #ffffff;
                }
                QCheckBox {
                    font-family: 'Segoe UI';
                    font-size: 10pt;
                    color: #ffffff;
                }
                QPushButton {
                    font-family: 'Segoe UI';
                    font-size: 9pt;
                    padding: 6px;
                    background-color: #3a3a3a;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
                QPushButton#btnLanzar {
                    font-family: 'Segoe UI';
                    font-size: 11pt;
                    font-weight: bold;
                    background-color: #0078D4;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px;
                }
                QPushButton#btnLanzar:hover {
                    background-color: #106EBE;
                }
                QComboBox {
                    font-family: 'Segoe UI';
                    font-size: 10pt;
                    background-color: #3a3a3a;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 2px;
                }
            """
            app.setStyleSheet(estilo_oscuro)

        else: # Claro
            estilo_claro = """
                QMainWindow, QWidget {
                    background-color: #f5f5f5;
                    color: #202020;
                    font-family: 'Segoe UI';
                }
                QToolBar {
                    background: transparent;
                    border: none;
                }
                QLabel {
                    color: #202020;
                }
                QGroupBox {
                    font-family: 'Segoe UI';
                    font-size: 10pt;
                    font-weight: bold;
                    border: 1px solid #c0c0c0;
                    border-radius: 6px;
                    margin-top: 10px;
                    padding-top: 15px;
                    color: #202020;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 5px;
                    color: #202020;
                }
                QCheckBox {
                    font-family: 'Segoe UI';
                    font-size: 10pt;
                    color: #202020;
                }
                QPushButton {
                    font-family: 'Segoe UI';
                    font-size: 9pt;
                    padding: 6px;
                    background-color: #e0e0e0;
                    color: #202020;
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton#btnLanzar {
                    font-family: 'Segoe UI';
                    font-size: 11pt;
                    font-weight: bold;
                    background-color: #0078D4;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px;
                }
                QPushButton#btnLanzar:hover {
                    background-color: #106EBE;
                }
                QComboBox {
                    font-family: 'Segoe UI';
                    font-size: 10pt;
                    background-color: #ffffff;
                    color: #202020;
                    border: 1px solid #c0c0c0;
                    border-radius: 4px;
                    padding: 2px;
                }
            """
            app.setStyleSheet(estilo_claro)

    def lanzar_apps(self):
        lanzadas = 0
        for app_name, chk in self.vars_apps.items():
            if chk.isChecked():
                lanzadas += 1
                config = APPS[app_name]
                try:
                    if isinstance(config, list):
                        subprocess.Popen(config)
                    else:
                        subprocess.Popen(config, shell=True)
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"No se pudo iniciar {app_name}:\n{e}"
                    )

        if lanzadas > 0:
            self.close()
        else:
            QMessageBox.warning(
                self, "Atención", "Selecciona al menos una aplicación."
            )