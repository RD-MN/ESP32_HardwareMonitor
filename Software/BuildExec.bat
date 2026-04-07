@echo off
title Build ESP32 Hardware Monitor Executable
echo ===========================================
echo Building ESP32 Hardware Monitor Single-File Executable
echo ===========================================

cd /d "%~dp0"

echo.
echo [1/3] Checking environment and dependencies...
if exist "..\env\Scripts\python.exe" (
    set "PYTHON_CMD=..\env\Scripts\python.exe"
    echo Using isolated Virtual Environment Python
) else (
    set "PYTHON_CMD=python"
    echo Using Global Python
)

REM Install PyInstaller and required modules into the environment
%PYTHON_CMD% -m pip install pypiwin32 pyinstaller pillow pythonnet pyserial pystray

echo.
echo [2/3] Preparing build configurations...
set OUT_DIR=ESP32 HWM
if exist "%OUT_DIR%" (
    echo Cleaning old build files...
    rmdir /s /q "%OUT_DIR%"
)
mkdir "%OUT_DIR%"

set ICON_ARG=
set ICON_DATA=
if exist "icon.ico" (
    echo Icon found! Including it in the executable...
    set ICON_ARG=-i "%~dp0icon.ico"
    set ICON_DATA=--add-data "%~dp0icon.ico;."
) else (
    echo No 'icon.ico' detected. Building with default executable icon.
)

REM We add the entire LHM directory into the payload
set ASSETS=--add-data "%~dp0..\LHM;LHM" %ICON_DATA%

REM Hidden imports to ensure nothing is missed (especially for plugins/system tray)
set HIDDEN_IMPORTS=--hidden-import serial.tools.list_ports --hidden-import pystray._win32

echo.
echo [3/3] Compiling Executable Payload...
%PYTHON_CMD% -m PyInstaller --clean --noconfirm --onefile --windowed --name "ESP32 Hardware Monitor" --distpath "%OUT_DIR%" --workpath "%OUT_DIR%\build" --specpath "%OUT_DIR%" %ICON_ARG% %ASSETS% %HIDDEN_IMPORTS% "LHMToSerial.py"

echo.
echo ===========================================
if exist "%OUT_DIR%\ESP32 Hardware Monitor.exe" (
    echo.
    echo SUCCESS: 'ESP32 Hardware Monitor.exe' created successfully!
    echo Location: %~dp0%OUT_DIR%\ESP32 Hardware Monitor.exe
    echo.
) else (
    echo ERROR: Build failed. Check the logs above.
)
echo ===========================================
pause
