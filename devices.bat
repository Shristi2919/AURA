@echo off
set ADB="C:\platform-tools\adb.exe"

echo Disconnecting old connections...
%ADB% disconnect

echo Setting up ADB over TCP/IP...
%ADB% tcpip 5555

echo Waiting for device to initialize...
timeout /t 3 /nobreak >nul

rem ── Set your phone IP here ──────────────────────────────
set ip=10.6.161.73
rem ────────────────────────────────────────────────────────

echo Connecting wirelessly to %ip%:5555 ...
%ADB% connect %ip%:5555

echo Done! ADB connected wirelessly.