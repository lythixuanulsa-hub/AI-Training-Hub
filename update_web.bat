@echo off
cd /d "%~dp0"
title TPM AI Training Hub - Cap nhat du lieu len Web

echo ============================================
echo    TPM AI TRAINING HUB - CAP NHAT LEN WEB
echo ============================================
echo.

echo [1/3] Dang kiem tra thay doi du lieu...
echo --------------------------------------------
git status -s training_data.csv documents.csv trainers.csv images/
echo --------------------------------------------
echo.

echo [2/3] Dang dong goi du lieu moi...
git add training_data.csv documents.csv trainers.csv images/
git commit -m "Cap nhat du lieu tu local dashboard"

echo.
echo [3/3] Dang dong bo len Web (GitHub)...
echo.
git push origin dev:main

echo.
echo ============================================
echo    DA DONG BO DU LIEU LEN WEB THANH CONG!
echo    Web truc tuyen se tu dong cap nhat sau 1-2 phut.
echo ============================================
echo.
pause
