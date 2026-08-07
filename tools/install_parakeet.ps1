# Vox2Book — install NVIDIA Parakeet TDT 0.6B v3 (onnx-asr, NOT Whisper)

Write-Host "Installing Parakeet STT stack (onnx-asr + onnxruntime)..." -ForegroundColor Cyan

py -3.11 tools\transcribe_audio.py --install-parakeet

Write-Host ""

Write-Host "First run downloads ~640 MB model to models\parakeet-tdt-0.6b-v3-int8\" -ForegroundColor Yellow

Write-Host "Usage:" -ForegroundColor Green

Write-Host "  .\transcribe_parakeet.bat inputs\audio\voice.ogg" -ForegroundColor Yellow

Write-Host "Or: py -3.11 tools\transcribe_audio.py inputs\audio\ --backend parakeet --language ru" -ForegroundColor Yellow

