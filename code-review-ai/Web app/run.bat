@echo off
REM Quick Start Script for Intelligent Code Review Assistant Dashboard (Windows)

echo.
echo 🚀 Starting Intelligent Code Review Assistant Dashboard...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies.
        echo    Please run manually: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo ==========================================
echo 🎯 Intelligent Code Review Assistant v2.0
echo ==========================================
echo.
echo ✅ Dependencies verified
echo.
echo 🌐 Starting Flask server...
echo    Dashboard will be available at:
echo.
echo    ➜ Local:   http://127.0.0.1:7860
echo    ➜ Network: http://0.0.0.0:7860
echo.
echo 📊 Features:
echo    • AI-powered code analysis using CodeBERT
echo    • Real-time explainability with token attribution
echo    • Automated code quality suggestions
echo    • Model evaluation metrics (accuracy, precision, recall, F1)
echo    • Dark theme professional dashboard
echo.
echo 📝 Tips:
echo    • Paste or upload your source code
echo    • Adjust sensitivity with threshold slider
echo    • Press Ctrl+Enter to analyze
echo    • Click 'Refresh' to update metrics
echo.
echo 🛑 To stop: Press Ctrl+C
echo.
echo ==========================================
echo.

REM Run the Flask app
python app.py

pause