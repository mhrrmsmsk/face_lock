@echo off
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
copy /Y "%~dp0dist\face_lock.exe" "%STARTUP%\face_lock.exe"
echo Başlangıca eklendi.
pause
