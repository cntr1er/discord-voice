@echo off

echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo An error occurred while installing dependencies. Exiting...
    pause
    exit /b
)

echo Dependencies installed successfully.
exit
