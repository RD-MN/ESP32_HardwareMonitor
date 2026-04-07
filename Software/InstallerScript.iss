[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
AppId={{144c2bdf-6e49-481e-92e9-376727df8f78}
AppName=ESP32 Hardware Monitor
AppVersion=1.0
AppPublisher=ESP32 HWM Community
DefaultDirName={autopf}\ESP32 Hardware Monitor
DefaultGroupName=ESP32 Hardware Monitor
AllowNoIcons=yes
; Output directory where the final Setup.exe will be placed
OutputDir=Installer Output
OutputBaseFilename=ESP32_Hardware_Monitor_Setup
SetupIconFile=icon.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\ESP32 Hardware Monitor.exe

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "ESP32 HWM\ESP32 Hardware Monitor.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ESP32 Hardware Monitor"; Filename: "{app}\ESP32 Hardware Monitor.exe"
Name: "{group}\{cm:UninstallProgram,ESP32 Hardware Monitor}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\ESP32 Hardware Monitor"; Filename: "{app}\ESP32 Hardware Monitor.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\ESP32 Hardware Monitor.exe"; Description: "{cm:LaunchProgram,ESP32 Hardware Monitor}"; Flags: nowait postinstall skipifsilent
