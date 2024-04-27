#!/bin/bash

# Define the target path for the pass50 executable
TARGET="$HOME/.local/bin/pass50"

# Download the latest version of pass50
wget https://raw.githubusercontent.com/zivmax/pass50/main/main.py -O ./pass50.py

# Check if the directory exists
if [ ! -d "$HOME/.local/bin" ]; then
    mkdir -p "$HOME/.local/bin"
fi

# Check if pass50 is already installed
if [ -f "$TARGET" ]; then
    is_update=true
else
    is_update=false
fi

# Move the file to the bin directory
cp ./pass50.py "$TARGET"
rm ./pass50.py
chmod +x "$TARGET"

# Provide user feedback based on installation or update
if [ "$is_update" = true ]; then
    echo "pass50 has been updated."
else
    echo "pass50 has been installed. Please run 'source ~/.profile' to update your PATH."
fi
