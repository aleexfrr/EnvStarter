import os
import sys
from datetime import datetime


def obtener_ruta_log():
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
    return os.path.join(base_dir, "envstarter.log")


def registrar_error(mensaje):
    """Registra un error genérico (ej. corrupción o fallo al leer el apps.ini)."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ruta_log = obtener_ruta_log()
    try:
        with open(ruta_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [ERROR] {mensaje}\n")
    except Exception as e:
        print(f"No se pudo escribir el log: {e}")


def registrar_fallo_lanzamiento(perfil, apps_intentadas, error_msg):
    """Registra el contexto completo si falla el lanzamiento de una app."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ruta_log = obtener_ruta_log()
    try:
        with open(ruta_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [ERROR] Fallo al lanzar entorno en perfil [{perfil}]\n")
            f.write(f"[{timestamp}] [INFO] Aplicaciones programadas para este lanzamiento:\n")
            for name, cmd in apps_intentadas:
                f.write(f"    - {name} ({cmd})\n")
            f.write(f"[{timestamp}] [ERROR] Detalle del error: {error_msg}\n")
            f.write("-" * 60 + "\n")
    except Exception as e:
        print(f"No se pudo escribir el log de fallo: {e}")