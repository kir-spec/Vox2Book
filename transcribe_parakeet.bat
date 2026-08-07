@echo off

chcp 65001 >nul

cd /d "%~dp0"

py -3.11 tools\transcribe_audio.py --backend parakeet --language ru %*

