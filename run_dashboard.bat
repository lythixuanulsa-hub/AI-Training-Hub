@echo off
cd /d "%~dp0"
echo Dang kiem tra Python va Streamlit...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python chua duoc cai dat hoac chua duoc them vao PATH.
    echo Vui long cai dat Python truoc.
    pause
    exit /b
)

echo Dang khoi dong ung dung LICH DAO TAO AI...
streamlit run app.py
pause
