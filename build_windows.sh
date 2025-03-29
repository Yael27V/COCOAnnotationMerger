#!/bin/bash

# Ensure we're in the correct folder
cd "$(dirname "$0")"

# Create virtual environment
python -m venv venv
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Run PyInstaller with custom .spec file
pyinstaller COCOAnnotationMerger.spec

echo "✅ Windows build complete. Executable is in the dist/ folder."
