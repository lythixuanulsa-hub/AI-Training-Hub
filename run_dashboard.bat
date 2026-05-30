@echo off
cd /d "%~dp0"
title TPM AI Training Hub - Dashboard

echo ============================================
echo    TPM AI TRAINING HUB - KHOI DONG APP
echo ============================================
echo.

:: Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LOI] Python chua duoc cai dat hoac chua duoc them vao PATH.
    echo Vui long cai dat Python truoc.
    pause
    exit /b
)

:: Kiem tra va tu dong giai phong cong 8501 neu bi chiem dung
echo Kiem tra cong 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do (
    echo [CANH BAO] Cong 8501 dang bi chiem dung boi PID %%a. Dang tu dong tat...
    taskkill /F /PID %%a >nul 2>&1
    echo      Da giai phong cong 8501 thanh cong!
)
echo.

:: Xoa cache Python cu
echo [1/3] Dang xoa cache Python cu...
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo      Da xoa __pycache__
) else (
    echo      Khong co cache Python.
)

:: Xoa cache Streamlit cu
echo [2/3] Dang xoa cache Streamlit cu...
if exist "%USERPROFILE%\.streamlit\cache" (
    rmdir /s /q "%USERPROFILE%\.streamlit\cache"
    echo      Da xoa Streamlit cache
) else (
    echo      Khong co Streamlit cache.
)

:: Khoi chay app
echo [3/3] Dang khoi dong ung dung...
echo.
echo ============================================
echo    App dang chay tai: http://localhost:8501
echo    Nhan Ctrl+C de dung app
echo ============================================
echo.

streamlit run app.py --server.runOnSave=true --server.port=8501

pause
