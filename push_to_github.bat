@echo off
title Slanje Porodicnog Stabla na GitHub
color 0b
echo =======================================================
echo    PORODICNO STABLO ZEHIC - SLANJE NA GITHUB
echo =======================================================
echo.
echo Repozitorij: https://github.com/zehicnermin-sudo/familytree.git
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    color 0a
    echo =======================================================
    echo    USPJESNO POSLANO NA GITHUB!
    echo =======================================================
    echo Sada mozete otvoriti https://vercel.com/new i kliknuti Deploy.
) else (
    color 0c
    echo =======================================================
    echo    DOSLO JE DO GRESKE PRI PRIJAVI
    echo =======================================================
)
echo.
pause
