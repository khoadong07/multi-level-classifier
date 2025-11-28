@echo off
echo Starting SPX Classification Backend...
echo.

REM Check if .env exists
if not exist "..\\.env" (
    echo Error: .env file not found
    echo Please create .env file from .env.example
    exit /b 1
)

REM Check if prompt_template.txt exists
if not exist "..\\prompt_template.txt" (
    echo Error: prompt_template.txt not found
    exit /b 1
)

echo All checks passed
echo Starting server on http://localhost:8000
echo API docs available at http://localhost:8000/docs
echo.

cd ..
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
