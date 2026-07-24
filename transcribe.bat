@echo off
chcp 65001 >nul
cd /d "%~dp0"
python tools\transcribe_audio.py %*
