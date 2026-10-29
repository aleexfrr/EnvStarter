import os

# Obtenemos la ruta del usuario actual de forma automática (ej: C:\Users\Usuario)
user_home = os.path.expanduser("~")

# Diccionario con el nombre visible y su ruta / comando de ejecución
DESARROLLO = {
    "VS Code": "code",
    "Fork": os.path.join(user_home, "AppData", "Local", "Fork", "current", "Fork.exe"),
    "Gemini": os.path.join(user_home, "AppData", "Local", "Google", "Gemini", "Gemini.exe"),
}

AUTOMATIZACION = {
    "HeidiSQL": os.path.join(user_home, "AppData", "Local", "Programs", "HeidiSQL", "heidisql.exe"),
    "Docker Desktop": r"C:\Program Files\Docker\Docker\Docker Desktop.exe",
    "Windows Terminal": "wt",
}

COMUNICACION = {
    "Microsoft Teams": "ms-teams",
    "Microsoft Edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
}