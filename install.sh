#!/bin/bash

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "'uv' not found. Installing 'uv'..."
    # Download and install uv script
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install 'uv'. Please install it manually."
        exit 1
    fi
    
    echo "'uv' installed successfully."
    
    # Ensure uv is in path for this session
    # Standard location is $HOME/.cargo/bin
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "'uv' is already installed."
fi

if [ -d ".venv" ]; then
    echo ".venv already exists."
    echo "Updating dependencies..."
    uv pip install "pyedb>=0.64.0" "pywebview>=6.1"
else
    echo ".venv not found. Setting up environment..."
    
    echo "Creating virtual environment..."
    uv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi

    echo "Installing dependencies..."
    uv pip install "pyedb>=0.64.0" "pywebview>=6.1"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies."
        exit 1
    fi
    
    echo "Setup complete!"
fi