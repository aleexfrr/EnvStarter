# 🚀 EnvStarter

Un lanzador de entornos de trabajo inteligente, ligero y moderno desarrollado en **Python y PyQt6**, diseñado para ingenieros y desarrolladores que necesitan arrancar su set de herramientas diario de forma ordenada, fluida y sin picos de rendimiento en el sistema.

---

## ✨ Características Principales

- **🗂️ Perfiles Múltiples Dinámicos:** Organiza tus aplicaciones por entornos (ej. *Desarrollo, Automatización, Redes*) mediante secciones en el archivo `.ini`. Crea nuevos perfiles al vuelo directamente desde la interfaz.
- **🎨 Iconos Reales del Sistema:** Extrae y muestra automáticamente el icono oficial incrustado en el archivo `.exe` o comando de cada aplicación (VS Code, Fork, Docker, LabVIEW, VIPM, etc.).
- **⏳ Lanzamiento Escalonado:** Abre las aplicaciones de forma secuencial con un retraso controlado (`400ms`), evitando congelamientos de Windows y evitando que las ventanas compitan por el foco.
- **📐 Ventana Dinámica con Scroll Inteligente:** La interfaz se adapta automáticamente a la cantidad de apps de cada perfil y activa una barra de desplazamiento limpia de forma natural a partir de 7-8 elementos.
- **⚙️ CRUD Completo:** Añade nuevas herramientas, edita rutas o nombres existentes y elimina aplicaciones de forma individual o múltiple desde la interfaz gráfica.
- **⚡ Selección Rápida:** Botones integrados para marcar o desmarcar todo el listado con un solo clic.
- **📝 Registro Condicional de Fallos (`envstarter.log`):** Genera automáticamente un log con contexto completo solo cuando ocurre un fallo al leer la configuración o al lanzar alguna aplicación.

---

## 📂 Estructura del Proyecto

```text
EnvStarter/
├── assets/
│   └── icon.ico          # Icono de la aplicación
├── src/
│   ├── __init__.py
│   ├── config_manager.py # Gestión del archivo apps.ini y perfiles
│   ├── dialog.py         # Ventanas emergentes (Añadir / Editar)
│   ├── gui.py            # Interfaz gráfica principal (PyQt6)
│   └── logger.py         # Registro condicional de errores y fallos de lanzamiento
├── build.bat             # Script de automatización de compilación con Nuitka
├── main.py               # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias del proyecto
└── README.md
```

---

## ⚙️ Requisitos e Instalación

Asegúrate de tener instalado **Python 3.x** en tu sistema (y un compilador de C compatible en Windows si vas a compilar con Nuitka). Luego, instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Compilación Automática con Nuitka (Recomendado)

EnvStarter utiliza **Nuitka** para compilar a un ejecutable nativo, evitando problemas de carpetas temporales `_MEI` o conflictos de entorno con herramientas externas como LabVIEW o VIPM.

Ejecuta el script `build.bat` desde la consola o haciendo doble clic en él:

```cmd
.\build.bat
```

El ejecutable resultante se generará en la carpeta `dist/EnvStarter.exe`.

---

## 📄 Configuración (`apps.ini`)

EnvStarter gestiona automáticamente sus configuraciones mediante un archivo `apps.ini` estructurado por perfiles junto al ejecutable o en la raíz del proyecto. Se generará automáticamente en el primer inicio si no existe.