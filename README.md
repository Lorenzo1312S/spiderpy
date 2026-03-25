# 🕷️ Pixel Spider

A cross-platform animated pixel art spider that crawls around your desktop.
Built with Python + PyQt6. Packaged as standalone executable (no dependencies needed).

## Platforms
- Windows ✅ (.exe)
- macOS ✅ (binary / .app)
- Linux ✅ (binary)

## Run from source
pip install PyQt6 psutil
python spider.py

## Build executable
pyinstaller --onefile --noconsole --add-data "assets:assets" --name spider spider.py