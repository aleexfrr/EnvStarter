import os
import sys
import subprocess
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QCheckBox, QDialog, QGroupBox, QHBoxLayout, QMainWindow,
    QMessageBox, QPushButton, QToolBar, QVBoxLayout, QWidget,
)
from src.config_manager import cargar_apps, eliminar_app
from src.dialog import ConfigDialog


class LanzadorApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EnvStarter - Panel de Control")
        self.setFixedSize(420, 520)

        icon_path = self._obtener_ruta_icono()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.vars_apps = {}
        self.apps_dict = {}
        self._crear_interfaz()
        self.cargar_lista_apps()

    def _obtener_ruta_icono(self):
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..")
            )
        return os.path.join(base_path, "assets", "icon.ico")

    def _crear_interfaz(self):
        # Barra superior con botones para añadir, borrar y editar apps
        toolbar = QToolBar("Barra Superior", self)
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        contenido_toolbar = QWidget(toolbar)
        layout_toolbar = QHBoxLayout(contenido_toolbar)
        layout_toolbar.setContentsMargins(0, 8, 0, 0)
        layout_toolbar.setSpacing(6)

        margen_toolbar_izquierdo = QWidget(contenido_toolbar)
        margen_toolbar_izquierdo.setFixedWidth(15)
        layout_toolbar.addWidget(margen_toolbar_izquierdo)

        # Botón Añadir
        btn_agregar = QPushButton(" ➕ Añadir ", self)
        btn_agregar.setStyleSheet(
            "font-size: 9pt; padding: 4px; border: 1px solid #c0c0c0; border-radius: 4px;"
        )
        btn_agregar.clicked.connect(self.abrir_dialogo_agregar)
        layout_toolbar.addWidget(btn_agregar)

        # Botón Editar
        btn_editar = QPushButton(" ✏️ Editar ", self)
        btn_editar.setStyleSheet(
            "font-size: 9pt; padding: 4px; border: 1px solid #c0c0c0; border-radius: 4px;"
        )
        btn_editar.clicked.connect(self.abrir_dialogo_editar)
        layout_toolbar.addWidget(btn_editar)

        # Botón Borrar
        btn_borrar = QPushButton(" 🗑️ Borrar ", self)
        btn_borrar.setStyleSheet(
            "font-size: 9pt; padding: 4px; border: 1px solid #c0c0c0; border-radius: 4px; color: #e84545;"
        )
        btn_borrar.clicked.connect(self.borrar_apps_seleccionada)
        layout_toolbar.addWidget(btn_borrar)

        margen_toolbar_derecho = QWidget(contenido_toolbar)
        margen_toolbar_derecho.setFixedWidth(15)
        layout_toolbar.addWidget(margen_toolbar_derecho)
        toolbar.addWidget(contenido_toolbar)

        toolbar.setStyleSheet(
            "QToolBar { background: transparent; border: none; }"
        )

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.layout_principal = QVBoxLayout(central_widget)
        self.layout_principal.setContentsMargins(20, 10, 20, 20)
        self.layout_principal.setSpacing(12)

        # --- CONTENEDOR DE APLICACIONES ---
        self.group_box = QGroupBox("Aplicaciones del Entorno de Trabajo")
        self.layout_group = QVBoxLayout(self.group_box)
        self.layout_group.setSpacing(8)
        self.layout_principal.addWidget(self.group_box)

        # --- BOTONES DE SELECCIÓN RÁPIDA ---
        layout_botones_sel = QHBoxLayout()
        self.btn_todos = QPushButton("Marcar todo", self)
        self.btn_todos.clicked.connect(self.seleccionar_todo)

        self.btn_ninguno = QPushButton("Desmarcar", self)
        self.btn_ninguno.clicked.connect(self.deseleccionar_todo)

        layout_botones_sel.addWidget(self.btn_todos)
        layout_botones_sel.addWidget(self.btn_ninguno)
        self.layout_principal.addLayout(layout_botones_sel)

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
        self.layout_principal.addWidget(self.btn_lanzar)

    def cargar_lista_apps(self):
        # Limpiar checkboxes anteriores
        for i in reversed(range(self.layout_group.count())):
            widget = self.layout_group.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.vars_apps.clear()
        self.apps_dict = cargar_apps()

        for app_name in self.apps_dict.keys():
            chk = QCheckBox(app_name, self)
            chk.setChecked(True)
            self.layout_group.addWidget(chk)
            self.vars_apps[app_name] = chk

    def abrir_dialogo_agregar(self):
        dialogo = ConfigDialog(self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.cargar_lista_apps()
            QMessageBox.information(
                self,
                "Éxito",
                "Aplicación añadida correctamente al archivo .ini",
            )

    def abrir_dialogo_editar(self):
        # Validar que haya exactamente una app seleccionada con el tick
        apps_marcadas = [
            name for name, chk in self.vars_apps.items() if chk.isChecked()
        ]

        if not apps_marcadas:
            QMessageBox.warning(
                self, "Atención", "Marca con el tick la aplicación que deseas editar."
            )
            return

        if len(apps_marcadas) > 1:
            QMessageBox.warning(
                self, "Atención", "Por favor, marca únicamente una aplicación para editar."
            )
            return

        app_name = apps_marcadas[0]
        comando_actual = self.apps_dict[app_name]

        # Abrir diálogo pasando los datos actuales
        dialogo = ConfigDialog(self, nombre_inicial=app_name, comando_inicial=comando_actual)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.cargar_lista_apps()
            QMessageBox.information(
                self,
                "Éxito",
                "Aplicación actualizada correctamente.",
            )

    def borrar_apps_seleccionada(self):
        # Ver qué aplicaciones tienen el tick marcado
        apps_marcadas = [
            name for name, chk in self.vars_apps.items() if chk.isChecked()
        ]

        if not apps_marcadas:
            QMessageBox.warning(
                self,
                "Atención",
                "Marca con el tick al menos una aplicación que deseas borrar.",
            )
            return

        # Crear una lista formateada con viñetas para el mensaje de confirmación
        lista_texto = "\n".join([f"• {app}" for app in apps_marcadas])

        mensaje = (
            f"¿Estás seguro de que deseas eliminar las siguientes "
            f"{len(apps_marcadas)} aplicaciones?\n\n{lista_texto}"
        )

        confirm = QMessageBox.question(
            self,
            "Confirmar eliminación",
            mensaje,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            for app_name in apps_marcadas:
                eliminar_app(app_name)
            
            self.cargar_lista_apps()
            QMessageBox.information(
                self,
                "Éxito",
                "Las aplicaciones seleccionadas han sido eliminadas correctamente.",
            )

    def seleccionar_todo(self):
        for chk in self.vars_apps.values():
            chk.setChecked(True)

    def deseleccionar_todo(self):
        for chk in self.vars_apps.values():
            chk.setChecked(False)

    def lanzar_apps(self):
        # Recopilar apps marcadas
        self.apps_a_lanzar = [
            (name, self.apps_dict[name])
            for name, chk in self.vars_apps.items() if chk.isChecked()
        ]

        if not self.apps_a_lanzar:
            QMessageBox.warning(
                self,
                "Atención",
                "Selecciona al menos una aplicación para lanzar.",
            )
            return

        # Deshabilitar botón para evitar doble clic y arrancar secuencia
        self.btn_lanzar.setEnabled(False)
        self.btn_lanzar.setText("⏳ Lanzando entorno...")
        self.indice_lanzamiento = 0
        self.lanzar_siguiente_app()

    def lanzar_siguiente_app(self):
        if self.indice_lanzamiento < len(self.apps_a_lanzar):
            app_name, comando = self.apps_a_lanzar[self.indice_lanzamiento]
            try:
                subprocess.Popen(comando, shell=True)
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"No se pudo iniciar {app_name}:\n{e}"
                )

            self.indice_lanzamiento += 1
            # 400ms de pausa entre app y app para evitar picos de CPU en Windows
            QTimer.singleShot(400, self.lanzar_siguiente_app)
        else:
            # Terminado el escalonado, cerramos la herramienta con suavidad
            self.close()