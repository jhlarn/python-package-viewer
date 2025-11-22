@echo off
if exist .venv (
    echo .venv already exists.
    echo Updating dependencies...
    uv pip install -e .
) else (
    echo .venv not found. Setting up environment...
    
    echo Creating virtual environment...
    uv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment. Is 'uv' installed?
        pause
        exit /b %errorlevel%
    )

    echo Installing dependencies...
    uv pip install -e .
    if %errorlevel% neq 0 (
        echo Error: Failed to install dependencies.
        pause
        exit /b %errorlevel%
    )
    
    echo Setup complete!
)
pause