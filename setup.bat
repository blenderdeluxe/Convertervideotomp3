@echo off
setlocal enabledelayedexpansion
title Configuracion - Convertidor Video a MP3

echo.
echo  =====================================================
echo    Convertidor de Video a MP3  ^|  Configuracion
echo  =====================================================
echo.
echo  Este asistente descargara automaticamente:
echo    - Python 3.11 (con soporte de interfaz grafica)
echo    - ffmpeg (motor de conversion de audio/video)
echo.
echo  Solo necesitas internet la primera vez.
echo.

REM ---------------------------------------------------------------
REM  Quick-check: skip if already configured
REM ---------------------------------------------------------------
if exist "python\python.exe" if exist "bin\ffmpeg.exe" (
    echo  [OK] La aplicacion ya esta configurada.
    echo       Ejecuta run.bat para iniciarla.
    echo.
    pause
    exit /b 0
)

REM ---------------------------------------------------------------
REM  Create working directories
REM ---------------------------------------------------------------
if not exist "python" mkdir python
if not exist "bin"    mkdir bin

REM ---------------------------------------------------------------
REM  STEP 1 – Download Python Embedded via NuGet package
REM           (includes tcl/tk libraries needed for the GUI)
REM ---------------------------------------------------------------
if not exist "python\python.exe" (
    echo  [1/3] Descargando Python 3.11 ...
    echo        ^(fuente: nuget.org – paquete oficial de Python^)
    echo.

    powershell -NoProfile -Command ^
      "$ProgressPreference='SilentlyContinue';" ^
      "Invoke-WebRequest -Uri 'https://globalcdn.nuget.org/packages/python.3.11.9.nupkg'" ^
      " -OutFile 'python-pkg.zip' -UseBasicParsing"

    if not exist "python-pkg.zip" (
        echo  ERROR: No se pudo descargar Python.
        echo         Verifica tu conexion a internet e intenta de nuevo.
        pause
        exit /b 1
    )

    echo  Extrayendo Python ...
    powershell -NoProfile -Command ^
      "Expand-Archive -Path 'python-pkg.zip' -DestinationPath 'python-pkg-tmp' -Force"

    REM The NuGet package lays everything under tools\
    if exist "python-pkg-tmp\tools\python.exe" (
        xcopy /E /I /Y "python-pkg-tmp\tools" "python\" >nul
    ) else (
        echo  ERROR: Estructura inesperada en el paquete de Python.
        rmdir /S /Q python-pkg-tmp 2>nul
        del /f /q python-pkg.zip 2>nul
        pause
        exit /b 1
    )

    rmdir /S /Q python-pkg-tmp
    del /f /q python-pkg.zip

    REM Enable site-packages so pip can install libraries
    set "PTH_FOUND=0"
    for %%F in (python\python3*._pth) do (
        powershell -NoProfile -Command ^
          "(Get-Content '%%F') -replace '#import site','import site' | Set-Content '%%F'"
        set "PTH_FOUND=1"
    )
    if "!PTH_FOUND!"=="0" (
        echo  ADVERTENCIA: No se encontro el archivo python3*._pth en la instalacion.
        echo               La aplicacion puede no funcionar correctamente.
    )

    REM Install pip
    echo  Instalando pip ...
    powershell -NoProfile -Command ^
      "$ProgressPreference='SilentlyContinue';" ^
      "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py'" ^
      " -OutFile 'get-pip.py' -UseBasicParsing"
    python\python.exe get-pip.py --quiet
    del /f /q get-pip.py
)
echo  [OK] Python listo.

REM ---------------------------------------------------------------
REM  STEP 2 – Download ffmpeg (static Windows build)
REM ---------------------------------------------------------------
if not exist "bin\ffmpeg.exe" (
    echo.
    echo  [2/3] Descargando ffmpeg ...
    echo        ^(puede tardar unos minutos segun tu velocidad de internet^)
    echo.

    powershell -NoProfile -Command ^
      "$ProgressPreference='SilentlyContinue';" ^
      "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'" ^
      " -OutFile 'ffmpeg.zip' -UseBasicParsing"

    if not exist "ffmpeg.zip" (
        echo  ERROR: No se pudo descargar ffmpeg.
        echo         Verifica tu conexion a internet e intenta de nuevo.
        pause
        exit /b 1
    )

    echo  Extrayendo ffmpeg ...
    powershell -NoProfile -Command ^
      "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg-tmp' -Force"

    REM Find ffmpeg.exe inside the extracted folder (name varies by version)
    for /r "ffmpeg-tmp" %%f in (ffmpeg.exe) do (
        copy /Y "%%f" "bin\ffmpeg.exe" >nul
    )

    rmdir /S /Q ffmpeg-tmp
    del /f /q ffmpeg.zip

    if not exist "bin\ffmpeg.exe" (
        echo  ERROR: No se encontro ffmpeg.exe en el archivo descargado.
        pause
        exit /b 1
    )
)
echo  [OK] ffmpeg listo.

REM ---------------------------------------------------------------
REM  STEP 3 – Verify the setup
REM ---------------------------------------------------------------
echo.
echo  [3/3] Verificando la instalacion ...
python\python.exe -c "import tkinter; print('  GUI (tkinter): OK')" 2>nul || (
    echo  ADVERTENCIA: No se pudo cargar la interfaz grafica ^(tkinter^).
    echo               La aplicacion puede no funcionar correctamente.
)
bin\ffmpeg.exe -version >nul 2>&1 && echo   ffmpeg:         OK

echo.
echo  =====================================================
echo    ^!Configuracion completada!
echo  =====================================================
echo.
echo   Para usar la aplicacion haz doble clic en:
echo     RUN.BAT
echo.
pause
