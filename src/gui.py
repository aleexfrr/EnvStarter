import os
import sys
import shutil
import subprocess
from PyQt6.QtCore import Qt, QTimer, QFileInfo
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QCheckBox, QDialog, QGroupBox, QHBoxLayout, QMainWindow,
    QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget, 
    QFileIconProvider, QComboBox, QLabel, QInputDialog
)
from src.config_manager import obtener_perfiles, cargar_apps, eliminar_app, crear_perfil
from src.dialog import ConfigDialog
from src.logger import registrar_error, registrar_fallo_lanzamiento


class LanzadorApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EnvStarter - Panel de Control")
        # Ancho fijo
        self.setMinimumWidth(420)
        self.setMaximumWidth(420)

        icon_path = self._obtener_ruta_icono()
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.vars_apps = {}
        self.apps_dict = {}
        self._crear_interfaz()
        self.cargar_perfiles()

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

        self.layout_principal = QVBoxLayout(central_widget)
        self.layout_principal.setContentsMargins(20, 10, 20, 20)
        self.layout_principal.setSpacing(12)

        # --- 1. SELECTOR DE PERFILES ---
        layout_perfil = QHBoxLayout()
        label_perfil = QLabel("Perfil activo:")
        label_perfil.setStyleSheet("font-weight: bold; font-size: 9.5pt;")
        layout_perfil.addWidget(label_perfil)

        self.combo_perfiles = QComboBox(self)
        self.combo_perfiles.setStyleSheet("padding: 4px; font-size: 9.5pt;")
        self.combo_perfiles.currentIndexChanged.connect(self.cambiar_perfil)
        layout_perfil.addWidget(self.combo_perfiles)

        # Botón para añadir un nuevo perfil rápidamente
        btn_nuevo_perfil = QPushButton("➕", self)
        btn_nuevo_perfil.setFixedWidth(32)
        btn_nuevo_perfil.setToolTip("Crear nuevo perfil")
        btn_nuevo_perfil.setStyleSheet("font-size: 9pt; padding: 4px;")
        btn_nuevo_perfil.clicked.connect(self.dialogo_crear_perfil)
        layout_perfil.addWidget(btn_nuevo_perfil)

        self.layout_principal.addLayout(layout_perfil)

        # --- 2. BOTONES DE ACCIÓN (Añadir, Editar, Borrar) ---
        layout_acciones = QHBoxLayout()
        layout_acciones.setSpacing(6)

        btn_agregar = QPushButton(" ➕ Añadir ", self)
        btn_agregar.setStyleSheet(
            "font-size: 9pt; padding: 5px; border: 1px solid #c0c0c0; border-radius: 4px;"
        )
        btn_agregar.clicked.connect(self.abrir_dialogo_agregar)
        layout_acciones.addWidget(btn_agregar)

        btn_editar = QPushButton(" ✏️ Editar ", self)
        btn_editar.setStyleSheet(
            "font-size: 9pt; padding: 5px; border: 1px solid #c0c0c0; border-radius: 4px;"
        )
        btn_editar.clicked.connect(self.abrir_dialogo_editar)
        layout_acciones.addWidget(btn_editar)

        btn_borrar = QPushButton(" 🗑️ Borrar ", self)
        btn_borrar.setStyleSheet(
            "font-size: 9pt; padding: 5px; border: 1px solid #c0c0c0; border-radius: 4px; color: #ff4d4d;"
        )
        btn_borrar.clicked.connect(self.borrar_apps_seleccionada)
        layout_acciones.addWidget(btn_borrar)

        self.layout_principal.addLayout(layout_acciones)

        # --- 3. CONTENEDOR DE APLICACIONES CON SCROLL ---
        self.group_box = QGroupBox("Aplicaciones del Entorno de Trabajo")
        group_layout = QVBoxLayout(self.group_box)
        group_layout.setContentsMargins(8, 12, 8, 8)

        # 1. Creamos el QScrollArea
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # 2. Widget contenedor interno que albergará los checkboxes dinámicos
        self.scroll_content = QWidget()
        self.layout_group = QVBoxLayout(self.scroll_content)
        self.layout_group.setSpacing(8)
        self.layout_group.setContentsMargins(5, 5, 5, 5)

        self.scroll_area.setWidget(self.scroll_content)
        group_layout.addWidget(self.scroll_area)
        
        self.layout_principal.addWidget(self.group_box)

        # --- 4. BOTONES DE SELECCIÓN RÁPIDA ---
        layout_botones_sel = QHBoxLayout()
        self.btn_todos = QPushButton("Marcar todo", self)
        self.btn_todos.clicked.connect(self.seleccionar_todo)

        self.btn_ninguno = QPushButton("Desmarcar", self)
        self.btn_ninguno.clicked.connect(self.deseleccionar_todo)

        layout_botones_sel.addWidget(self.btn_todos)
        layout_botones_sel.addWidget(self.btn_ninguno)
        self.layout_principal.addLayout(layout_botones_sel)

        # --- 5. BOTÓN PRINCIPAL DE LANZAMIENTO ---
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

    def cargar_perfiles(self):
        self.combo_perfiles.blockSignals(True)
        self.combo_perfiles.clear()
        perfiles = obtener_perfiles()
        self.combo_perfiles.addItems(perfiles)
        self.combo_perfiles.blockSignals(False)
        
        if perfiles:
            self.cargar_lista_apps()

    def cambiar_perfil(self):
        self.cargar_lista_apps()

    def dialogo_crear_perfil(self):
        nombre, ok = QInputDialog.getText(
            self, "Nuevo Perfil", "Introduce el nombre del nuevo perfil (ej: Oficina, Redes):"
        )
        if ok and nombre.strip():
            nombre_limpio = nombre.strip()
            perfiles_actuales = obtener_perfiles()
            
            if nombre_limpio in perfiles_actuales:
                QMessageBox.warning(self, "Atención", f"El perfil '{nombre_limpio}' ya existe.")
                return

            crear_perfil(nombre_limpio)
            self.cargar_perfiles()
            
            # Seleccionar automáticamente el perfil recién creado
            index = self.combo_perfiles.findText(nombre_limpio)
            if index >= 0:
                self.combo_perfiles.setCurrentIndex(index)
                
            QMessageBox.information(
                self, "Éxito", f"Perfil '{nombre_limpio}' creado correctamente."
            )

    def obtener_icono_app(self, comando):
        """Extrae el icono real del ejecutable mediante la API de Windows / QFileIconProvider"""
        cmd_limpio = comando.strip('"\'')
        # Si es un comando del sistema como 'code' o 'wt', buscamos su ruta absoluta en PATH
        ruta_real = shutil.which(cmd_limpio) or cmd_limpio
        
        if os.path.exists(ruta_real):
            file_info = QFileInfo(ruta_real)
            provider = QFileIconProvider()
            return provider.icon(file_info)
        return QIcon()  # Icono vacío por defecto si no se encuentra archivo físico

    def cargar_lista_apps(self):
        # Limpiar checkboxes anteriores
        for i in reversed(range(self.layout_group.count())):
            widget = self.layout_group.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.vars_apps.clear()
        perfil_actual = self.combo_perfiles.currentText()
        self.apps_dict = cargar_apps(perfil_actual)

        for app_name, comando in self.apps_dict.items():
            chk = QCheckBox(app_name, self)
            chk.setChecked(True)
            
            # Asignar el icono real del ejecutable al checkbox
            icono = self.obtener_icono_app(comando)
            if not icono.isNull():
                chk.setIcon(icono)

            self.layout_group.addWidget(chk)
            self.vars_apps[app_name] = chk

        # --- ALTURA DINÁMICA INTELIGENTE ---
        num_apps = len(self.apps_dict)
        # 280px para los elementos fijos (perfiles, botones, márgenes) + ~32px por cada app
        altura_calculada = 280 + (num_apps * 32)
        
        # Mínimo 360px para listas pequeñas, máximo 520px
        altura_final = max(360, min(altura_calculada, 520))
        
        # Ajustamos el tamaño de la ventana al vuelo
        self.resize(420, altura_final)

    def abrir_dialogo_agregar(self):
        perfil_actual = self.combo_perfiles.currentText()
        dialogo = ConfigDialog(self, perfil_actual=perfil_actual)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.cargar_lista_apps()
            QMessageBox.information(
                self,
                "Éxito",
                f"Aplicación añadida correctamente al perfil [{perfil_actual}].",
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
        perfil_actual = self.combo_perfiles.currentText()

        dialogo = ConfigDialog(
            self, 
            perfil_actual=perfil_actual, 
            nombre_inicial=app_name, 
            comando_inicial=comando_actual
        )
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
            perfil_actual = self.combo_perfiles.currentText()
            for app_name in apps_marcadas:
                eliminar_app(perfil_actual, app_name)
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
        perfil_actual = self.combo_perfiles.currentText()
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

        # Guardamos el perfil actual por si ocurre algún fallo durante la secuencia
        self.perfil_lanzamiento = perfil_actual

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
                error_msg = f"No se pudo iniciar '{app_name}' con comando '{comando}': {e}"
                
                # Si falla, registramos el contexto completo y el error
                registrar_fallo_lanzamiento(self.perfil_lanzamiento, self.apps_a_lanzar, error_msg)
                
                QMessageBox.critical(
                    self, "Error", f"No se pudo iniciar {app_name}:\n{e}"
                )

            self.indice_lanzamiento += 1
            # 400ms de pausa entre app y app para evitar picos de CPU en Windows
            QTimer.singleShot(400, self.lanzar_siguiente_app)
        else:
            # Terminado el escalonado, cerramos la herramienta con suavidad
            self.close()