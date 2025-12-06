@echo off
if not exist .venv (
    echo Environment not set up. Please run install.bat first.
    pause
    exit /b
)
start "" ".venv\Scripts\python.exe" main.py
exit
