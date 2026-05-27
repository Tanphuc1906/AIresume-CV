@echo off
echo ==========================================
echo    Khoi chay AI Resume Agent
echo ==========================================

echo Dang khoi dong Giao dien Streamlit...
start "AI Resume Agent" cmd /k "call .\venv\Scripts\activate.bat && streamlit run frontend\app.py --server.address=127.0.0.1"

echo ==========================================
echo Ung dung dang khoi chay o cua so moi.
echo Truy cap tai: http://127.0.0.1:8501
echo ==========================================
pause
