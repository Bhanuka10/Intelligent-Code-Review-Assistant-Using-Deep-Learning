#!/bin/bash
# Quick Start Script for Intelligent Code Review Assistant Dashboard

echo "🚀 Starting Intelligent Code Review Assistant Dashboard..."
echo ""

# Navigate to the Web app directory
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please run: pip install -r requirements.txt"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "🎯 Intelligent Code Review Assistant v2.0"
echo "=========================================="
echo ""
echo "✅ Dependencies verified"
echo ""
echo "🌐 Starting Flask server..."
echo "   Dashboard will be available at:"
echo ""
echo "   ➜ Local:   http://127.0.0.1:7860"
echo "   ➜ Network: http://0.0.0.0:7860"
echo ""
echo "📊 Features:"
echo "   • AI-powered code analysis using CodeBERT"
echo "   • Real-time explainability with token attribution"
echo "   • Automated code quality suggestions"
echo "   • Model evaluation metrics (accuracy, precision, recall, F1)"
echo "   • Dark theme professional dashboard"
echo ""
echo "📝 Tips:"
echo "   • Paste or upload your source code"
echo "   • Adjust sensitivity with threshold slider"
echo "   • Press Ctrl+Enter to analyze"
echo "   • Click 'Refresh' to update metrics"
echo ""
echo "🛑 To stop: Press Ctrl+C"
echo ""
echo "=========================================="
echo ""

# Run the Flask app
python3 app.py