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

echo [4/4] Compilando ejecutable con PyInstaller...
pyinstaller --noconsole ^
    --onefile ^
    --clean ^
    --noconfirm ^
    --icon=assets/icon.ico ^
    --add-data "assets;assets" ^
    --name="EnvStarter" ^
    --distpath dist ^
    --workpath build ^
    --exclude-module tkinter ^
    --exclude-module unittest ^
    --exclude-module pydoc ^
    main.py || exit /b 1

call deactivate

echo.
echo =========================================
echo    [EXITO] Compilacion completada!
echo    Ejecutable generado en: dist\EnvStarter.exe
echo =========================================
echo.
pause
endlocal