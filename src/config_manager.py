import configparser
import os
import sys
from src.config import DESARROLLO, AUTOMATIZACION, COMUNICACION
from src.logger import registrar_error


def obtener_ruta_ini():
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
    return os.path.join(base_dir, "apps.ini")


def obtener_configuracion():
    config = configparser.ConfigParser()
    config.optionxform = str
    path = obtener_ruta_ini()

    # Si no existe el archivo .ini, lo creamos con valores por defecto
    if not os.path.exists(path):
        try:
            config["Desarrollo"] = DESARROLLO
            config["Automatización"] = AUTOMATIZACION
            config["Comunicación"] = COMUNICACION
            with open(path, "w", encoding="utf-8") as f:
                config.write(f)
        except Exception as e:
            registrar_error(f"No se pudo crear el archivo 'apps.ini' por defecto: {e}")
            return config

    # Intentamos leer y parsear el archivo con control de excepciones
    try:
        config.read(path, encoding="utf-8")
    except configparser.Error as e:
        registrar_error(f"Error de sintaxis o formato en el archivo 'apps.ini': {e}")
    except Exception as e:
        registrar_error(f"Error inesperado al leer el archivo 'apps.ini': {e}")

    return config


def obtener_perfiles():
    config = obtener_configuracion()
    perfiles = config.sections()
    if not perfiles:
        perfiles = ["Desarrollo"]
    return perfiles


def cargar_apps(perfil):
    config = obtener_configuracion()
    if config.has_section(perfil):
        return dict(config[perfil])
    return {}


def guardar_nueva_app(perfil, nombre, comando):
    config = obtener_configuracion()
    if not config.has_section(perfil):
        config.add_section(perfil)
    
    config.set(perfil, nombre, comando)
    path = obtener_ruta_ini()
    try:
        with open(path, "w", encoding="utf-8") as f:
            config.write(f)
    except Exception as e:
        registrar_error(f"Error al guardar nueva aplicación en 'apps.ini': {e}")


def editar_app(perfil, nombre_antiguo, nuevo_nombre, nuevo_comando):
    config = obtener_configuracion()
    if config.has_section(perfil):
        if nombre_antiguo != nuevo_nombre and config.has_option(perfil, nombre_antiguo):
            config.remove_option(perfil, nombre_antiguo)
        
        config.set(perfil, nuevo_nombre, nuevo_comando)
        path = obtener_ruta_ini()
        try:
            with open(path, "w", encoding="utf-8") as f:
                config.write(f)
        except Exception as e:
            registrar_error(f"Error al editar aplicación en 'apps.ini': {e}")


def eliminar_app(perfil, nombre):
    config = obtener_configuracion()
    if config.has_section(perfil) and config.has_option(perfil, nombre):
        config.remove_option(perfil, nombre)
        path = obtener_ruta_ini()
        try:
            with open(path, "w", encoding="utf-8") as f:
                config.write(f)
        except Exception as e:
            registrar_error(f"Error al eliminar aplicación en 'apps.ini': {e}")


def crear_perfil(nombre_perfil):
    config = obtener_configuracion()
    if not config.has_section(nombre_perfil):
        config.add_section(nombre_perfil)
        path = obtener_ruta_ini()
        try:
            with open(path, "w", encoding="utf-8") as f:
                config.write(f)
        except Exception as e:
            registrar_error(f"Error al crear el perfil '{nombre_perfil}' en 'apps.ini': {e}")