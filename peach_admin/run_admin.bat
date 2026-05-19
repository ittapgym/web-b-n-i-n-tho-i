@echo off
title MangoAdmin Desktop
color 0A

echo.
echo  ==========================================
echo    MANGOSTORE ADMIN DESKTOP
echo    PC Application - Electron
echo  ==========================================
echo.

cd /d "%~dp0"

:: Cai dependencies neu chua co
if not exist "node_modules" (
    echo  Dang cai dat dependencies, vui long cho...
    npm install
    echo  Cai dat xong!
    echo.
)

echo  Dang khoi dong MangoAdmin Desktop...
npm start
