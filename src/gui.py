import tkinter as tk
import subprocess
from tkinter import messagebox
from src.config import APPS

class LanzadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lanzador de Aplicaciones")
        self.root.geometry("340x380")
        self.root.resizable(False, False)

        self.vars_apps = {}
        self._construir_interfaz()

    def _construir_interfaz(self):
        # Título
        lbl_titulo = tk.Label(
            self.root,
            text="¿Qué arrancamos hoy?",
            font=("Segoe UI", 12, "bold"),
            pady=10,
        )
        lbl_titulo.pack()

        # Contenedor para los Checkbuttons
        frame_checks = tk.Frame(self.root, padx=20)
        frame_checks.pack(anchor="w")

        for app_name in APPS.keys():
            var = tk.IntVar(value=1)  # Por defecto marcadas
            chk = tk.Checkbutton(
                frame_checks,
                text=app_name,
                variable=var,
                font=("Segoe UI", 10),
                anchor="w",
            )
            chk.pack(anchor="w", pady=2)
            self.vars_apps[app_name] = var

        # Botones de selección rápida
        frame_botones_sel = tk.Frame(self.root, pady=5)
        frame_botones_sel.pack()

        btn_todos = tk.Button(
            frame_botones_sel, text="Marcar todo", command=self.seleccionar_todo, width=12
        )
        btn_todos.pack(side=tk.LEFT, padx=5)

        btn_ninguno = tk.Button(
            frame_botones_sel, text="Desmarcar", command=self.deseleccionar_todo, width=12
        )
        btn_ninguno.pack(side=tk.RIGHT, padx=5)

        # Botón Principal de Lanzamiento
        btn_lanzar = tk.Button(
            self.root,
            text="🚀 Lanzar Seleccionadas",
            command=self.lanzar_apps,
            font=("Segoe UI", 10, "bold"),
            bg="#0078D4",
            fg="white",
            padx=10,
            pady=5,
        )
        btn_lanzar.pack(pady=15)

    def seleccionar_todo(self):
        for var in self.vars_apps.values():
            var.set(1)

    def deseleccionar_todo(self):
        for var in self.vars_apps.values():
            var.set(0)

    def lanzar_apps(self):
        lanzadas = 0
        for app_name, var in self.vars_apps.items():
            if var.get() == 1:  # Si está marcada
                lanzadas += 1
                config = APPS[app_name]
                try:
                    if isinstance(config, list):
                        # Caso especial para Edge con URLs
                        subprocess.Popen(config)
                    else:
                        # Aplicaciones normales o comandos de consola
                        subprocess.Popen(config, shell=True)
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"No se pudo iniciar {app_name}:\n{e}"
                    )

        if lanzadas > 0:
            self.root.destroy()  # Cierra la interfaz al terminar de lanzar
        else:
            messagebox.showwarning(
                "Atención", "Selecciona al menos una aplicación."
            )