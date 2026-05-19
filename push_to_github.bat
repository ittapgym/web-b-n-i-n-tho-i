@echo off
title DONG GOI VA UP CODE LEN GITHUB - PEACH STORE
color 0B

echo ======================================================================
echo           PEACH STORE - HE THONG DONG GOI VA DAY CODE LEN GITHUB      
echo ======================================================================
echo.
echo [*] Dang kiem tra trang thai Git cuc bo...

:: Kiem tra thu muc .git
if not exist .git (
    echo [!] Chua tim thay kho luu tru Git cuc bo. Dang khoi tao...
    git init
    echo.
) else (
    echo [ok] Da tim thay kho luu tru Git cuc bo.
)

:: Thiet lap remote URL chinh xac
echo [*] Dang cau hinh lien ket voi GitHub:
echo     Link repo: https://github.com/ittapgym/web-b-n-i-n-tho-i.git
git remote remove origin >nul 2>&1
git remote add origin https://github.com/ittapgym/web-b-n-i-n-tho-i.git
echo [ok] Cau hinh Remote thanh cong!
echo.

:: Cho phep nguoi dung nhap thong diep commit
echo ======================================================================
set /p commit_msg="👉 Nhap thong diep Commit (Nhan Enter de dung mac dinh): "

if "%commit_msg%"=="" (
    set commit_msg=Cap nhat Peach Store - Ban nang cap Premium [Google Map, Social Icons, Newsletter]
)
echo.
echo [*] Dang dong goi tat ca cac file du an...
git add .

echo [*] Dang luu tru phien ban Commit voi thong diep:
echo     "%commit_msg%"
git commit -m "%commit_msg%"
echo.

echo [*] Dang dong bo hoa cau truc nhanh 'main'...
git branch -M main
echo.

echo ======================================================================
echo          DANG TIEN HANH DAY MA NGUON LEN GITHUB. VUI LONG DOI...      
echo ======================================================================
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] MA NGUON DA DUOC TAI LEN GITHUB HOAN TAT!
    echo Repo Link: https://github.com/ittapgym/web-b-n-i-n-tho-i
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo [ERROR] Co loi xay ra trong qua trinh day code len GitHub.
    echo Goi y khac phuc:
    echo   1. Hay chac chan rang ban da dang nhap Git tren may tinh.
    echo   2. Co the co popup dang nhap hien len, hay bam dang nhap de xac thuc.
    echo ======================================================================
)
echo.
pause
