@echo off
REM One-time setup / repair for the LED control. OpenRGB is the engine.
REM Self-elevates so OpenRGB can load its driver and detect the ASUS board + devices.
net session >nul 2>&1
if %errorlevel% neq 0 (
  powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)
set "ORGB=C:\Program Files\OpenRGB\OpenRGB.exe"
if not exist "%ORGB%" (
  echo Installing OpenRGB via winget...
  winget install --id OpenRGB.OpenRGB -e --accept-package-agreements --accept-source-agreements
)
if not exist "%ORGB%" for /f "delims=" %%i in ('where OpenRGB.exe 2^>nul') do set "ORGB=%%i"
echo.
echo Detected RGB devices (elevated):
"%ORGB%" --list-devices
echo.
echo If devices are listed above, leds-off.cmd / leds-white.cmd will work.
echo If the list is empty, your board may need OpenRGB opened once from the Start Menu.
pause
