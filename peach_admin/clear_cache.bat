@echo off
title Peach Admin Cache Cleaner
color 0B

echo.
echo  ======================================================
echo    PEACH ADMIN CACHE CLEANER
echo    Don sach Cache, LocalStorage, Cookies & Sessions
echo  ======================================================
echo.

echo  [1/3] Dang dong cac tien trinh Peach Admin dang chay ngam...
taskkill /F /IM electron.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo  [2/3] Dang xoa toan bo thu muc cache AppData (Roaming & Local)...
set "cleared=0"
if exist "%APPDATA%\PeachAdmin" (
    rmdir /S /Q "%APPDATA%\PeachAdmin"
    echo   -= DA XOA SACH CACHE ROAMING TAi: %APPDATA%\PeachAdmin =-
    set "cleared=1"
)
if exist "%LOCALAPPDATA%\PeachAdmin" (
    rmdir /S /Q "%LOCALAPPDATA%\PeachAdmin"
    echo   -= DA XOA SACH CACHE LOCAL TAi: %LOCALAPPDATA%\PeachAdmin =-
    set "cleared=1"
)
if "%cleared%"=="0" (
    echo   Khong co file cache nao can xoa. Bo nho dem da sach se tu truoc!
)

echo  [3/3] Hoan tat cac buoc lam sach...
timeout /t 1 /nobreak >nul

echo.
echo  ======================================================
echo   KHOI PHUC CACHE THANH CONG! MOI THU DA TUOI MOI!
echo  ======================================================
echo.

set /p choice="Ban co muon KHOI DONG LAI ung dung ngay lap tuc khong? (Y/N): "
if /i "%choice%"=="y" (
    echo.
    echo  Dang mo lai Peach Admin...
    cd /d "%~dp0"
    npm start
) else (
    echo.
    echo  Xong! Nhan phim bat ky de thoat...
    pause >nul
)
