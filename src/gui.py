import os
import sys
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from src.config import APPS


class LanzadorApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EnvStarter - Panel de Control")
        self.setFixedSize(420, 460)

        # Cargar icono de forma segura (compatible con desarrollo y ejecutable portátil)
        icon_path = self._obtener_ruta_icono()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.vars_apps = {}
        self._crear_interfaz()

    def _obtener_ruta_icono(self):
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..")
            )
        return os.path.join(base_path, "assets", "icon.ico")

    def _crear_interfaz(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout_principal = QVBoxLayout(central_widget)
        layout_principal.setContentsMargins(20, 20, 20, 20)
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
        self.btn_lanzar.setStyleSheet("""
            QPushButton {
                font-family: 'Segoe UI';
                font-size: 11pt;
                font-weight: bold;
                background-color: #0078D4;
                color: white;
                border-radius: 6px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
        """)
        self.btn_lanzar.clicked.connect(self.lanzar_apps)
        layout_principal.addWidget(self.btn_lanzar)

    def seleccionar_todo(self):
        for chk in self.vars_apps.values():
            chk.setChecked(True)

    def deseleccionar_todo(self):
        for chk in self.vars_apps.values():
            chk.setChecked(False)

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