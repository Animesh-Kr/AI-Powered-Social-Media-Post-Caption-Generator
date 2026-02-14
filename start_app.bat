@echo off
REM Quick Start Script for AI Content Generator
REM This script ensures the app runs with the correct conda environment

echo ========================================
echo   AI Content Generator - Quick Start
echo ========================================
echo.

REM Check if conda is available
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda not found in PATH
    echo Please install Anaconda or Miniconda
    pause
    exit /b 1
)

echo [1/3] Activating GPU_RTX environment...
call conda activate GPU_RTX
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate GPU_RTX environment
    echo Create it with: conda create -n GPU_RTX python=3.11
    pause
    exit /b 1
)

echo [2/3] Checking dependencies...
python -c "import streamlit; import torch; import transformers" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Some dependencies missing
    echo Installing required packages...
    pip install -r requirements.txt
)

echo [3/3] Launching Streamlit app...
echo.
echo ========================================
echo   App will open in your browser
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

REM Use python -m to ensure correct environment
python -m streamlit run app.py

pause
