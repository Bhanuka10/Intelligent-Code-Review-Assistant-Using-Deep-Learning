# ⚡ Quick Reference Card

## 🚀 START HERE

### Launch Dashboard (Choose One)

**macOS/Linux:**
```bash
cd "/Users/jin/Desktop/projects/Intelligent-Code-Review-Assistant-Using-Deep-Learning/code-review-ai/Web app"
./run.sh
```

**Windows:**
```cmd
cd "C:\Users\...\code-review-ai\Web app"
run.bat
```

**Manual:**
```bash
python3 app.py
```

### 📱 Access Dashboard
```
http://127.0.0.1:7860
```

---

## 🎯 Basic Workflow

1. **Paste Code** → Code editor
2. **Select Language** (optional) → Python, Java, JS, C++, etc.
3. **Adjust Threshold** (optional) → 0-1 slider (lower = more sensitive)
4. **Click Analyze** → Wait 0.8-1.2 seconds
5. **Review Results** → Prediction, confidence, tokens, suggestions

---

## 🎨 What's New (Features)

| Feature | Purpose |
|---------|---------|
| 🌙 Dark Theme | Professional developer aesthetic |
| 📝 Code Editor | Paste or upload source code |
| 📊 Metrics Dashboard | Accuracy, Precision, Recall, F1 |
| 🔍 Explainability | See top influential tokens |
| 💡 Suggestions | AI-generated code fixes |
| 📜 History | Last 10 analyses |
| ⌨️ Shortcuts | Ctrl+Enter (analyze), Ctrl+K (focus) |
| 📱 Responsive | Desktop, tablet, mobile optimized |

---

## 📂 Key Files

```
Web app/
├── Template/Index.html          (Dashboard UI - 208 lines)
├── Static/Style.css             (Dark theme - 1074 lines)
├── Static/Script.js             (Interactions - 384 lines)
├── app.py                       (Flask server - 66 lines)
├── model_interface.py           (AI model - 284 lines)
├── requirements.txt             (Dependencies)
├── run.sh / run.bat             (Launchers)
└── Documentation/
    ├── DASHBOARD_GUIDE.md       (User guide)
    ├── FEATURES_SHOWCASE.md     (Feature details)
    └── ARCHITECTURE.md          (Technical docs)
```

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Kill the process using port 7860
lsof -i :7860 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Model Loading Slow
- First run: 2-3 minutes (downloads 500MB model)
- Subsequent runs: Fast (cached locally)

### High Latency
- Normal: 0.8-1.2 seconds per analysis
- GPU support: Install CUDA version of PyTorch

### Memory Issues
- Reduce batch size in `model_interface.py`
- Close other applications

---

## ⌨️ Keyboard Shortcuts

| Keys | Action |
|------|--------|
| `Ctrl+Enter` | Analyze code (from editor) |
| `Ctrl+K` | Focus code editor |
| `Tab` | Navigate controls |
| `Escape` | Dismiss messages |

---

## 📊 Understanding Results

### Prediction Badge
- 🚨 **DEFECTIVE** (Red) = Code contains potential issues
- ✓ **CLEAN** (Green) = Code appears safe

### Confidence Gauge
- **90-100%** = Very high confidence
- **70-89%** = High confidence
- **50-69%** = Moderate confidence
- **<50%** = Low confidence (review manually)

### Metrics
- **Accuracy** = % correct predictions
- **Precision** = % of flagged defects that are real
- **Recall** = % of actual defects detected
- **F1** = Balance between precision & recall

---

## 🔗 API Endpoints

### POST /analyze
```bash
curl -X POST http://127.0.0.1:7860/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "def foo(): pass", "threshold": 0.5}'
```

### GET /metrics
```bash
curl http://127.0.0.1:7860/metrics
# Add ?recompute=true to recalculate
```

### GET /health
```bash
curl http://127.0.0.1:7860/health
```

---

## 🎨 Customization

### Change Colors
Edit `Static/Style.css`:
```css
:root {
  --primary: #2563eb;        /* Main blue */
  --success: #10b981;        /* Green for clean */
  --danger: #ef4444;         /* Red for defects */
  /* More colors available */
}
```

### Change Default Threshold
Edit `Static/Script.js`:
```javascript
thresholdInput.value = 0.6;  // From 0.5
```

### Add More Languages
Edit `Template/Index.html`:
```html
<option value="scala">Scala</option>
<option value="kotlin">Kotlin</option>
```

---

## 📈 Performance

| Operation | Time |
|-----------|------|
| Page load | <500ms |
| Code analysis | 0.8-1.2s |
| Metrics load | 50-100ms |
| Model download | 2-3 min (first run only) |

---

## 🔐 Security

### What It Does
✅ Analyzes code (doesn't execute it)
✅ Uses pre-trained model (frozen)
✅ Validates inputs
✅ Prevents XSS attacks

### What It Doesn't Do
❌ Run your code
❌ Store code on server
❌ Modify your files
❌ Send code to cloud

---

## 📚 Learn More

| Document | Content |
|----------|---------|
| **DASHBOARD_GUIDE.md** | Complete user guide |
| **FEATURES_SHOWCASE.md** | Feature details & examples |
| **ARCHITECTURE.md** | Technical & deployment info |

---

## 💡 Pro Tips

1. **Paste Complete Code** - Fragments give less accurate results
2. **Use Proper Formatting** - Well-formatted code analyzes better
3. **Review Suggestions** - AI suggestions are recommendations, verify manually
4. **Adjust Threshold** - Lower for development, higher for production
5. **Check Metrics** - Understand model confidence from metrics dashboard

---

## 🚀 What's Next

### To Deploy to Production
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:7860 app:app
```

### To Add Database Persistence
See ARCHITECTURE.md → "Scalability & Future Improvements"

### To Fine-Tune Model
- Notebook: `03_model_training.ipynb`
- Use your own labeled dataset
- Update checkpoint location

---

## 📞 Common Questions

**Q: How accurate is the model?**
A: ~56% accuracy on test set. Use as first-pass filter, always review manually.

**Q: What languages does it support?**
A: Trained on C/C++. Works on Python, Java, JS, Go, Rust with variable accuracy.

**Q: Is my code stored anywhere?**
A: No. Code only used for analysis, not persisted to disk or sent elsewhere.

**Q: Can I use this offline?**
A: Yes! After first run (when model is cached). Works completely offline.

**Q: How do I improve accuracy?**
A: Fine-tune on your own code dataset using notebook `03_model_training.ipynb`.

---

## 🎯 Success Criteria

Your dashboard is working if:

✅ Server starts without errors
✅ http://127.0.0.1:7860 loads
✅ Can paste code
✅ Analyze button works
✅ Results appear in <2 seconds
✅ Metrics dashboard shows numbers
✅ Dark theme looks professional

---

## ⚡ One-Liner Commands

```bash
# Start server
./run.sh

# Kill server
Ctrl+C

# Check status
curl http://127.0.0.1:7860/health

# Analyze code (curl)
curl -X POST http://127.0.0.1:7860/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"int x = 1/0;","threshold":0.5}'
```

---

**Version**: 2.0 | **Status**: ✅ Production Ready | **Last Updated**: May 2026