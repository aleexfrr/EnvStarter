@echo off
setlocal
cd /d "%~dp0"

echo =========================================
echo    EnvStarter - Compilador Automatico
echo =========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH.
    pause
    exit /b 1
)

if not exist .venv (
    echo [1/4] Creando entorno virtual...
    python -m venv .venv || exit /b 1
) else (
    echo [1/4] Entorno virtual detectado.
)

echo [2/4] Activando entorno virtual...
call .venv\Scripts\activate.bat || exit /b 1

echo [3/4] Instalando / Actualizando dependencias...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt || exit /b 1

echo [4/4] Compilando ejecutable con Nuitka...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=disable ^
    --enable-plugin=pyqt6 ^
    --include-data-dir=assets=assets ^
    --windows-icon-from-ico=assets/icon.ico ^
    --file-description="Environment Starter" ^
    --product-name="EnvStarter" ^
    --file-version=1.7.0.0 ^
    --product-version=1.7.0.0 ^
    --copyright="Copyright © 2026 RANDIS" ^
    --output-filename=EnvStarter.exe ^
    --output-dir=dist ^
    main.py

if errorlevel 1 (
    echo [ERROR] Fallo en la compilacion con Nuitka.
    exit /b 1
)

call deactivate

echo.
echo =========================================
echo    [EXITO] Compilacion completada!
echo    Ejecutable generado en: dist\EnvStarter.exe
echo =========================================
echo.
pause
endlocal