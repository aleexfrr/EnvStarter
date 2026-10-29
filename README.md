# 🚀 EnvStarter

Un lanzador de entornos de trabajo inteligente, ligero y moderno desarrollado en **Python y PyQt6**, diseñado para ingenieros y desarrolladores que necesitan arrancar su set de herramientas diario de forma ordenada, fluida y sin picos de rendimiento en el sistema.

---

## ✨ Características Principales

* **🗂️ Perfiles Múltiples Dinámicos:** Organiza tus aplicaciones por entornos (ej. *Desarrollo, Automatización, Redes*) mediante secciones en el archivo `.ini`. Crea nuevos perfiles al vuelo directamente desde la interfaz.
* **🎨 Iconos Reales del Sistema:** Extrae y muestra automáticamente el icono oficial incrustado en el archivo `.exe` o comando de cada aplicación (VS Code, Fork, Docker, etc.).
* **⏳ Lanzamiento Escalonado:** Abre las aplicaciones de forma secuencial con un retraso controlado (`400ms`), evitando congelamientos de Windows y evitando que las ventanas compitan por el foco.
* **📐 Ventana Dinámica con Scroll Inteligente:** La interfaz se adapta automáticamente a la cantidad de apps de cada perfil y activa una barra de desplazamiento limpia de forma natural a partir de 7-8 elementos.
* **⚙️ CRUD Completo:** Añade nuevas herramientas, edita rutas o nombres existentes y elimina aplicaciones de forma individual o múltiple desde la interfaz gráfica.
* **⚡ Selección Rápida:** Botones integrados para marcar o desmarcar todo el listado con un solo clic.

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
├── main.py               # Punto de entrada de la aplicación
└── README.md
```

---

## ⚙️ Requisitos e Instalación

Asegúrate de tener instalado **Python 3.x** en tu sistema. Luego, instala las dependencias necesarias:

```bash
pip install -r .\requirements.txt
```

---

## 📦 Generar Ejecutable (.exe)

EnvStarter incluye soporte para compilarse en un único archivo ejecutable portátil utilizando **PyInstaller**. 

Ejecuta el siguiente comando en la raíz del proyecto para generar el `.exe` empaquetando automáticamente los recursos multimedia:

```shell
pyinstaller --noconsole --onefile --icon=assets/icon.ico --add-data "assets;assets" --name="EnvStarter" main.py
```

El ejecutable resultante estará disponible dentro de la carpeta `dist/`.

---

## 📄 Configuración (`apps.ini`)

EnvStarter gestiona automáticamente sus configuraciones mediante un archivo `apps.ini` estructurado por perfiles en la raíz de la aplicación. Se generará solo en el primer inicio con una plantilla inicial de ejemplo.
