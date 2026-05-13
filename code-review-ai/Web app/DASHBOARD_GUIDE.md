# Intelligent Code Review Assistant - Dashboard Guide

## 🎯 Overview

The **Intelligent Code Review Assistant** is a modern, professional web-based dashboard powered by CodeBERT deep learning model. It provides real-time AI-powered code analysis with explainability, automated suggestions, and comprehensive evaluation metrics.

## ✨ Features

### 1. **Modern UI Design**
- Dark developer-style theme inspired by GitHub Copilot and SonarQube
- Responsive layout optimized for desktop and tablet
- Smooth animations and transitions
- Professional card-based components
- Syntax-highlighted code editor

### 2. **Code Input Section**
- **Large Code Editor**: Paste or type your source code with monospace font
- **Language Selection**: Choose from Python, JavaScript, Java, C++, C, Go, Rust
- **File Upload**: Drag-and-drop or click to upload source files (.py, .js, .java, .cpp, .c, .go, .rs)
- **Character Counter**: Real-time display of code length
- **Clear Button**: Quickly reset the code editor
- **Line Numbering**: Built-in editor features

### 3. **AI Analysis Results**
- **Prediction Verdict**: Clear indication of DEFECTIVE or CLEAN classification
- **Confidence Gauge**: Visual progress bar showing model confidence
- **Probability Cards**: Separate displays for defect and clean probabilities
- **Top Influential Tokens**: Shows which code tokens triggered the detection
- **Automated Suggestions**: AI-generated fixes and recommendations

### 4. **Explainability**
- **Token Attribution**: Displays the most important tokens that influenced the prediction
- **Gradient-Based Attribution**: Uses Integrated Gradients from Captum library
- **Human-Readable Explanations**: Understand why the code was flagged

### 5. **Model Evaluation Metrics**
- **Accuracy**: Overall correctness of predictions
- **Precision**: True positive rate among positive predictions
- **Recall**: Coverage of actual positive cases
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Full breakdown of TP, TN, FP, FN

### 6. **Scan History**
- **Recent Scans**: Last 10 analyses with timestamps
- **Quick Review**: See prediction and confidence for previous scans
- **Code Preview**: First 50 characters of analyzed code

### 7. **Threshold Control**
- **Dynamic Sensitivity**: Adjust defect probability threshold from 0.0 to 1.0
- **Real-Time Updates**: Change sensitivity while analyzing
- **Visual Feedback**: Slider with numeric display

## 🚀 Getting Started

### Installation

1. **Navigate to Web App Directory**
   ```bash
   cd "/Users/jin/Desktop/projects/Intelligent-Code-Review-Assistant-Using-Deep-Learning/code-review-ai/Web app"
   ```

2. **Ensure Dependencies are Installed**
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - Flask 3.0+
   - PyTorch
   - Transformers
   - Scikit-learn
   - Pandas
   - NumPy

### Running the Dashboard

```bash
python app.py
```

The application will start on **http://127.0.0.1:7860**

Access it in your browser:
- **Local Machine**: http://127.0.0.1:7860
- **Network Access**: http://0.0.0.0:7860 (available to other devices on your network)

## 📝 Usage Guide

### Step 1: Input Code
```
Option A: Paste directly
- Click the code editor
- Paste your source code
- Supports any programming language

Option B: Upload file
- Click "Upload File" button
- Select a .py, .js, .java, .cpp, .c, .go, or .rs file
- File content auto-loads into editor
```

### Step 2: Select Language (Optional)
```
- Choose your programming language from dropdown
- Helps with syntax highlighting and tokenization
```

### Step 3: Adjust Threshold (Optional)
```
- Default: 0.50 (balanced detection)
- Lower threshold (0.0-0.3): More sensitive, detects more potential issues
- Higher threshold (0.7-1.0): More conservative, fewer false positives
```

### Step 4: Analyze Code
```
Click "Analyze Code" button
- Or press Ctrl+Enter on keyboard
```

### Step 5: Review Results
```
Prediction Card:
- Shows verdict (DEFECTIVE/CLEAN)
- Displays confidence percentage
- Probability breakdown

Explainability:
- Top influential tokens highlighted
- Gradient attribution scores
- Understand model's reasoning

Suggestions:
- Automated recommendations
- Pattern-based security warnings
- Code quality improvements
```

## 🧠 Model Details

### Architecture
- **Base Model**: CodeBERT (microsoft/codebert-base)
- **Encoder**: Frozen transformer layers (125M parameters)
- **Classification Head**: Trainable MLP (200K parameters)
- **Training**: 3 epochs on frozen encoder
- **Optimization**: AdamW with learning rate 1e-3

### Performance
- **Accuracy**: ~56.2%
- **Precision**: ~56.5%
- **Recall**: ~20.4%
- **F1-Score**: ~30.0%

### Dataset
- **Training**: ~9,000 code snippets
- **Validation**: ~2,000 code snippets
- **Testing**: ~2,000 code snippets
- **Task**: Binary classification (CLEAN vs DEFECTIVE)

## 🔍 Interpreting Results

### Prediction Confidence
- **90-100%**: Very high confidence
- **70-89%**: High confidence
- **50-69%**: Moderate confidence
- **< 50%**: Low confidence (use with caution)

### Severity Levels
The model identifies several issue categories:
- **Critical**: Buffer overflows, use-after-free, SQL injection
- **High**: Memory leaks, infinite loops, race conditions
- **Medium**: Code smells, inefficient patterns
- **Low**: Style issues, naming conventions

### Token Importance
- Tokens with higher scores are stronger indicators
- Special tokens ([CLS], [SEP], etc.) are filtered
- Top 12 tokens are displayed for clarity

## ⚙️ Configuration

### Adjusting Detection Sensitivity
1. Move threshold slider left for more detections
2. Move threshold slider right for fewer detections
3. Reanalyze code to see updated results

### Refreshing Metrics
- Click "Refresh" button to recompute evaluation metrics
- Loads metrics from test dataset (samples ~300 for speed)
- Cached metrics available for instant access

## 🔗 API Endpoints

### POST /analyze
Analyze source code and get predictions.

**Request:**
```json
{
  "code": "def divide(a, b):\n    return a / b",
  "threshold": 0.5
}
```

**Response:**
```json
{
  "prediction": "DEFECTIVE",
  "confidence": 0.92,
  "defect_prob": 0.92,
  "clean_prob": 0.08,
  "explainability": {
    "top_tokens": [
      {"token": "/", "score": 0.45},
      {"token": "divide", "score": 0.38}
    ]
  },
  "suggestions": [
    "Add validation for zero division",
    "Consider using try-except block"
  ]
}
```

### GET /metrics
Get model evaluation metrics.

**Response:**
```json
{
  "accuracy": 0.5622,
  "precision": 0.5651,
  "recall": 0.2040,
  "f1_score": 0.2998,
  "confusion_matrix": [[500, 100], [150, 300]],
  "source": "test_clean.csv",
  "samples": 950
}
```

### GET /health
Check model and system status.

**Response:**
```json
{
  "status": "ok",
  "device": "cpu",
  "checkpoint": "/Users/.../best_model.pt",
  "model": "microsoft/codebert-base"
}
```

## 📊 Understanding the Metrics Panel

| Metric | Meaning | Target |
|--------|---------|--------|
| **Accuracy** | Correct predictions / Total predictions | > 85% |
| **Precision** | Correct defects / Predicted defects | > 80% |
| **Recall** | Detected defects / Actual defects | > 75% |
| **F1-Score** | Harmonic mean of precision & recall | > 0.75 |

### Confusion Matrix
```
                 Predicted
                Clean | Defect
Actual Clean    TP   | FP
       Defect   FN   | TN
```
- **True Positives (TP)**: Correctly identified defects
- **False Negatives (FN)**: Missed defects (Type II error)
- **False Positives (FP)**: Incorrectly flagged clean code (Type I error)
- **True Negatives (TN)**: Correctly identified clean code

## 🎨 Dark Theme Colors

| Element | Color | Hex |
|---------|-------|-----|
| Background | Dark Blue | #0f172a |
| Card Background | Secondary Dark | #1e293b |
| Primary Button | Blue | #2563eb |
| Success | Green | #10b981 |
| Warning | Amber | #f59e0b |
| Danger | Red | #ef4444 |
| Text Primary | Light Gray | #f1f5f9 |
| Text Secondary | Gray | #cbd5e1 |

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+Enter** | Analyze code (from code editor) |
| **Ctrl+K** | Focus code editor |
| **Escape** | Close status messages |

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(host="0.0.0.0", port=8080)
```

### Model Loading Slow
- First run downloads CodeBERT from Hugging Face (~500MB)
- Subsequent runs load from cache (~30 seconds startup)
- Model will display "Loading weights..." message

### High Latency on Analysis
- Model inference takes ~2-3 seconds
- First request initializes GPU/CPU (slightly slower)
- For batch analysis, use `/analyze` API endpoint

### Metrics Not Loading
- Ensure test dataset exists at `notebooks/data/test_clean.csv`
- Click "Refresh" button to recompute
- Check browser console (F12) for error messages

## 📈 Performance Optimization

### For Production
1. **Use GPU**: Install PyTorch with CUDA support
2. **Batch Processing**: Use API for multiple analyses
3. **Caching**: Implement Redis for metric caching
4. **Load Balancing**: Deploy with Gunicorn/uWSGI

### For Development
1. **Hot Reload**: Flask auto-reloads on code changes
2. **Debug Mode**: Enabled by default (app.py)
3. **Terminal Logging**: All requests logged to stdout

## 🔐 Security Notes

- ⚠️ **Development Mode**: Enabled by default
- ⚠️ **Input Validation**: Implemented but not production-hardened
- ⚠️ **API Access**: No authentication (add for production)
- ✅ **Model Safety**: Uses pre-trained CodeBERT (no arbitrary code execution)
- ✅ **Code Isolation**: Analysis doesn't execute user code

## 📚 Additional Resources

- **CodeBERT**: https://github.com/microsoft/CodeBERT
- **Transformers**: https://huggingface.co/transformers/
- **PyTorch**: https://pytorch.org/
- **Captum**: https://captum.ai/

## 💡 Tips for Best Results

1. **Provide Complete Code**: Use full functions, not fragments
2. **Standard Formats**: Works best with well-formatted code
3. **Known Languages**: Model trained on C/C++ primarily
4. **Adjust Threshold**: Lower for development, higher for production
5. **Review Suggestions**: AI suggestions are recommendations, verify manually

## 🚀 Next Steps

- **Extend Model**: Fine-tune on your own code dataset
- **Add Custom Rules**: Integrate with linters (ESLint, Pylint)
- **Batch Analysis**: Implement async job queue
- **Export Reports**: Generate PDF review reports
- **Team Integration**: Connect to GitHub/GitLab webhooks

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review browser console (F12)
3. Check backend logs in terminal
4. Verify all dependencies installed

---

**Dashboard Version**: 2.0
**Last Updated**: May 2026
**Model**: CodeBERT Base
**Framework**: Flask + Vanilla JavaScript