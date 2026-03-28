@echo off
cd /d "%~dp0"

if not exist "python\python.exe" (
    echo La aplicacion no esta configurada.
    echo Haz doble clic en setup.bat para instalarla primero.
    echo.
    pause
    exit /b 1
)

if not exist "bin\ffmpeg.exe" (
    echo ffmpeg no encontrado.
    echo Haz doble clic en setup.bat para instalarlo.
    echo.
    pause
    exit /b 1
)

python\python.exe app.py
