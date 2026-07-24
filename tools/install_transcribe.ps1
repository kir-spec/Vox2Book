#Requires -Version 5.1
# Vox2Book — установка зависимостей для распознавания речи (Windows)
Set-Location $PSScriptRoot\..
Write-Host "Vox2Book: installing Whisper / faster-whisper dependencies..." -ForegroundColor Cyan
python tools/transcribe_audio.py --install
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""
Write-Host "Done. Put audio in inputs/audio/ and run:" -ForegroundColor Green
Write-Host "  .\transcribe.bat inputs\audio\your_file.mp3" -ForegroundColor Yellow
Write-Host "Or: python tools/transcribe_audio.py --list-models" -ForegroundColor Yellow
