@echo off
setlocal

echo Checking for 'uv' installation...
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo 'uv' not found. Installing 'uv'...
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    if %errorlevel% neq 0 (
        echo Error: Failed to install 'uv'. Please install it manually.
        pause
        exit /b 1
    )
    echo 'uv' installed successfully.
    :: Refresh environment variables in the current session so 'uv' can be found
    set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
) else (
    echo 'uv' is already installed.
)

if exist .venv (
    echo .venv already exists.
    echo Updating dependencies...
    uv pip install -e .
) else (
    echo .venv not found. Setting up environment...
    
    echo Creating virtual environment...
    uv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
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
