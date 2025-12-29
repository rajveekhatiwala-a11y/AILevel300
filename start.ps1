# Enterprise RAG Document Q&A System - Startup Script
# This script helps you start the application easily

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Enterprise RAG Document Q&A System" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$pipList = pip list
if ($pipList -notmatch "fastapi") {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "Dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "Dependencies already installed!" -ForegroundColor Green
}

# Check if .env file exists
if (-Not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "WARNING: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file from .env.example and add your Azure credentials" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Steps:" -ForegroundColor Yellow
    Write-Host "1. Copy .env.example to .env" -ForegroundColor White
    Write-Host "2. Edit .env and add your Azure credentials" -ForegroundColor White
    Write-Host "3. Run this script again" -ForegroundColor White
    Write-Host ""
    
    $createEnv = Read-Host "Do you want to create .env file now? (Y/N)"
    if ($createEnv -eq "Y" -or $createEnv -eq "y") {
        Copy-Item .env.example .env
        Write-Host ".env file created! Please edit it and add your credentials." -ForegroundColor Green
        notepad .env
        exit
    } else {
        exit
    }
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Starting Application..." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The application will be available at:" -ForegroundColor Green
Write-Host "  http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
