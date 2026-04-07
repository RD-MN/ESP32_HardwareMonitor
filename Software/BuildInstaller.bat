@echo off
title Build ESP32 Hardware Monitor Installer
echo ===========================================
echo Building Installer for ESP32 Hardware Monitor
echo ===========================================

cd /d "%~dp0"

echo.
echo [1/2] Checking for Single-File Executable...
if not exist "ESP32 HWM\ESP32 Hardware Monitor.exe" (
    echo ERROR: Could not find 'ESP32 Hardware Monitor.exe' in 'ESP32 HWM' directory.
    echo Please run BuildExec.bat first to generate the executable!
    echo.
    pause
    exit /b 1
)
echo Found executable!

echo.
echo [2/2] Compiling Installer using Inno Setup...

REM Try common installation paths for Inno Setup 6
set "ISCC_PATH="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
) else if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=%ProgramFiles%\Inno Setup 6\ISCC.exe"
) else if exist "%LocalAppData%\Programs\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=%LocalAppData%\Programs\Inno Setup 6\ISCC.exe"
)

if "%ISCC_PATH%"=="" (
    echo ERROR: Inno Setup 6 Compiler ^(ISCC.exe^) was not found.
    echo To build this installer, you need to download and install Inno Setup.
    echo Please visit: https://jrsoftware.org/isinfo.php
    echo After installing, run this script again.
    echo.
    pause
    exit /b 1
)

echo Found Inno Setup Compiler at: %ISCC_PATH%
"%ISCC_PATH%" "InstallerScript.iss"

echo.
echo ===========================================
if exist "Installer Output\ESP32_Hardware_Monitor_Setup.exe" (
    echo SUCCESS: Installer created successfully!
    echo Location: %~dp0Installer Output\ESP32_Hardware_Monitor_Setup.exe
) else (
    echo ERROR: Installer creation failed.
)
echo ===========================================
pause
