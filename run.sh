#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "Environment not set up. Please run ./install.sh first."
    exit 1
fi

# Run in background and disown to detach from terminal (similar to pythonw behavior)
nohup .venv/bin/python main.py > /dev/null 2>&1 &
