# Vox2Book — запуск одной командой
# Usage:
#   .\run.ps1                    — авто (берёт первый файл из inputs/raw_texts/)
#   .\run.ps1 file.txt           — конкретный файл
#   .\run.ps1 file.txt out.docx  — файл + выход

param(
    [string]$InputFile = "",
    [string]$OutputFile = ""
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

Write-Host "=== Vox2Book — Редакторский отдел ===" -ForegroundColor Cyan
Write-Host ""

# Проверка Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
    Write-Host "ОШИБКА: Python не найден. Установите Python 3.10+." -ForegroundColor Red
    exit 1
}

# Проверка python-docx
$checkDocx = & $python.Source -c "import docx; print('ok')" 2>&1
if ($checkDocx -ne "ok") {
    Write-Host "Установка python-docx..." -ForegroundColor Yellow
    & $python.Source -m pip install python-docx --quiet
}

# Если файл не указан — ищем в inputs/raw_texts/
if ($InputFile -eq "") {
    $rawFiles = Get-ChildItem "inputs/raw_texts" -Filter *.txt -ErrorAction SilentlyContinue
    if ($rawFiles.Count -eq 0) {
        $rawFiles = Get-ChildItem "inputs/raw_texts" -Filter *.md -ErrorAction SilentlyContinue
    }
    if ($rawFiles.Count -eq 0) {
        Write-Host "Нет файлов в inputs/raw_texts/. Положите .txt файл туда." -ForegroundColor Yellow
        exit 1
    }
    $InputFile = $rawFiles[0].FullName
    Write-Host "Авто-выбран файл: $InputFile" -ForegroundColor Green
}

# Запуск pipeline
$args = @()
if ($InputFile) { $args += $InputFile }
if ($OutputFile) { $args += $OutputFile }

Write-Host "Запуск конвейера..." -ForegroundColor Cyan
Write-Host ""
& $python.Source pipeline.py @args

Write-Host ""
Write-Host "Готово. Результат в output/books/" -ForegroundColor Green