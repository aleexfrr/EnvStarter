import configparser
import os
import sys
from src.config import APPS


def obtener_ruta_ini():
    # Si está compilado como .exe, guarda el .ini al lado del ejecutable
    # Si está en desarrollo, lo guarda en la raíz del proyecto EnvStarter/
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
    return os.path.join(base_dir, "apps.ini")


def cargar_apps():
    config = configparser.ConfigParser()
    config.optionxform = str
    path = obtener_ruta_ini()

    # Si no existe el archivo .ini, lo creamos con valores por defecto
    if not os.path.exists(path):
        user_home = os.path.expanduser("~")
        config["Apps"] = APPS
        with open(path, "w", encoding="utf-8") as f:
            config.write(f)

    config.read(path, encoding="utf-8")
    return dict(config["Apps"])


def guardar_nueva_app(nombre, comando):
    config = configparser.ConfigParser()
    config.optionxform = str
    path = obtener_ruta_ini()
    config.read(path, encoding="utf-8")

    if not config.has_section("Apps"):
        config.add_section("Apps")

    config.set("Apps", nombre, comando)
    with open(path, "w", encoding="utf-8") as f:
        config.write(f)

def editar_app(nombre_antiguo, nuevo_nombre, nuevo_comando):
    config = configparser.ConfigParser()
    config.optionxform = str
    path = obtener_ruta_ini()
    config.read(path, encoding="utf-8")

    if config.has_section("Apps"):
        # Si cambiaron el nombre, borramos la clave antigua
        if nombre_antiguo != nuevo_nombre and config.has_option("Apps", nombre_antiguo):
            config.remove_option("Apps", nombre_antiguo)

        config.set("Apps", nuevo_nombre, nuevo_comando)
        with open(path, "w", encoding="utf-8") as f:
            config.write(f)

def eliminar_app(nombre):
    config = configparser.ConfigParser()
    config.optionxform = str
    path = obtener_ruta_ini()
    config.read(path, encoding="utf-8")

    if config.has_section("Apps") and config.has_option("Apps", nombre):
        config.remove_option("Apps", nombre)
        with open(path, "w", encoding="utf-8") as f:
            config.write(f)