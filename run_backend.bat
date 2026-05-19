@echo off
echo Dang khoi dong Peach Store Backend...
start http://127.0.0.1:8000/docs
cd backend
call venv\Scripts\activate
uvicorn app.main:app --reload
pause
