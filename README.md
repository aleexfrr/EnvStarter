# 🚀 EnvStarter

Un lanzador de entornos de trabajo inteligente, ligero y moderno desarrollado en **Python y PyQt6**, diseñado para ingenieros y desarrolladores que necesitan arrancar su set de herramientas diario de forma ordenada, fluida y sin picos de rendimiento en el sistema.

---

## ✨ Características Principales

- **🗂️ Perfiles Múltiples Dinámicos:** Organiza tus aplicaciones por entornos (ej. *Desarrollo, Automatización, Redes*) mediante secciones en el archivo `.ini`. Crea nuevos perfiles al vuelo directamente desde la interfaz.
- **🎨 Iconos Reales del Sistema:** Extrae y muestra automáticamente el icono oficial incrustado en el archivo `.exe` o comando de cada aplicación (VS Code, Fork, Docker, etc.).
- **⏳ Lanzamiento Escalonado:** Abre las aplicaciones de forma secuencial con un retraso controlado (`400ms`), evitando congelamientos de Windows y evitando que las ventanas compitan por el foco.
- **📐 Ventana Dinámica con Scroll Inteligente:** La interfaz se adapta automáticamente a la cantidad de apps de cada perfil y activa una barra de desplazamiento limpia de forma natural a partir de 7-8 elementos.
- **⚙️ CRUD Completo:** Añade nuevas herramientas, edita rutas o nombres existentes y elimina aplicaciones de forma individual o múltiple desde la interfaz gráfica.
- **⚡ Selección Rápida:** Botones integrados para marcar o desmarcar todo el listado con un solo clic.

---

## 📂 Estructura del Proyecto

```text
EnvStarter/
├── assets/
│   └── icon.ico          # Icono de la aplicación
├── src/
│   ├── __init__.py
│   ├── config_manager.py # Gestión del archivo apps.ini y perfiles
│   ├── dialogs.py        # Ventanas emergentes (Añadir / Editar)
│   └── gui.py            # Interfaz gráfica principal (PyQt6)
├── build.bat             # Script de automatización de compilación
├── main.py               # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias del proyecto
└── README.md
```

---

## ⚙️ Requisitos e Instalación

Asegúrate de tener instalado **Python 3.x** en tu sistema. Luego, instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Compilación Automática (Recomendado)

EnvStarter incluye un script `build.bat` que automatiza todo el proceso de compilación. Simplemente haz doble clic en `build.bat` o ejecútalo desde la consola:

```cmd
.\build.bat
```

Este script se encarga de:
1. Crear automáticamente un entorno virtual local (`.venv`) si no existe.
2. Instalar y actualizar todas las dependencias (`requirements.txt`).
3. Compilar el proyecto con **PyInstaller** optimizado sin consola y empaquetando los recursos (`assets`).
4. Generar el ejecutable listo para usar en la carpeta `dist/EnvStarter.exe`.

---

## 📦 Compilación Manual con PyInstaller

Si prefieres compilar manualmente el ejecutable portátil sin usar el script de automatización, puedes ejecutar el siguiente comando en la raíz del proyecto:

```shell
pyinstaller --noconsole --onefile --clean --noconfirm --icon=assets/icon.ico --add-data "assets;assets" --name="EnvStarter" main.py
```

El ejecutable resultante estará disponible dentro de la carpeta `dist/`.

---

## 📄 Configuración (`apps.ini`)

EnvStarter gestiona automáticamente sus configuraciones mediante un archivo `apps.ini` estructurado por perfiles en la raíz de la aplicación. Se generará solo en el primer inicio con una plantilla inicial de ejemplo.
