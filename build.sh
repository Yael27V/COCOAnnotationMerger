#!/bin/bash

set -e

APP_NAME="COCOAnnotationMerger"
APP_DIR="AppDir"
DIST_DIR="dist"

echo "🔧 Cleaning previous builds..."
rm -rf build/ $DIST_DIR/ $APP_DIR/ __pycache__/

echo "📁 Creating AppDir structure..."
mkdir -p $APP_DIR/usr/bin
mkdir -p $APP_DIR/usr/share/applications
mkdir -p $APP_DIR/usr/share/icons/hicolor/256x256/apps
mkdir -p $DIST_DIR

echo "🐍 Creating virtual environment inside AppDir..."
python3 -m venv $APP_DIR/usr/bin/env
source $APP_DIR/usr/bin/env/bin/activate

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo "🚀 Building with PyInstaller..."
pyinstaller app/main.py \
    --name $APP_NAME \
    --noconfirm \
    --onefile \
    --distpath $APP_DIR/usr/bin \
    --paths app/ \
    --add-data "assets:assets"

echo "📄 Creating .desktop file..."
cat > $APP_DIR/usr/share/applications/$APP_NAME.desktop <<EOF
[Desktop Entry]
Name=COCO Annotation Merger
Exec=$APP_NAME
Icon=logo
Type=Application
Categories=Utility;
EOF

echo "🖼️ Copying icon..."
cp assets/logo.png $APP_DIR/usr/share/icons/hicolor/256x256/apps/logo.png

echo "📦 Downloading linuxdeploy and AppImage plugin..."
wget -q https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-x86_64.AppImage

echo "📦 Packaging AppImage..."
./linuxdeploy-x86_64.AppImage --appdir $APP_DIR \
    -d $APP_DIR/usr/share/applications/$APP_NAME.desktop \
    -i $APP_DIR/usr/share/icons/hicolor/256x256/apps/logo.png \
    --output appimage

echo "📁 Moving AppImage to dist/"
mv *.AppImage $DIST_DIR/

echo "✅ Done! Find your AppImage in the '$DIST_DIR/' folder."
