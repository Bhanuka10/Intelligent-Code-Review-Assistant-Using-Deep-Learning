# Intelligent Code Review Web App

This web app provides an automated code review dashboard backed by a transformer-based deep learning model.

## Features

- Source-code defect prediction (`CLEAN` / `DEFECTIVE`)
- Confidence and class probabilities
- Token-level explainability (top influential tokens)
- Rule-assisted review suggestions (bugs, code smells, inefficiency hints)
- Evaluation metrics endpoint (accuracy, precision, recall, F1, confusion matrix)

## Project Structure

- `app.py`: Flask app routes and API endpoints
- `model_interface.py`: Model loading, inference, explainability, metrics computation
- `Template/Index.html`: Dashboard UI
- `Static/Script.js`: Frontend logic
- `Static/Style.css`: Styling

## Run

```bash
cd "/Users/jin/Desktop/projects/Intelligent-Code-Review-Assistant-Using-Deep-Learning/code-review-ai/Web app"
python -m pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:7860`

## API Endpoints

- `GET /` - Dashboard
- `POST /analyze` - Analyze source code
- `GET /metrics` - Return cached or computed metrics
- `GET /health` - Health status

### `/analyze` request body

```json
{
  "code": "int main(){return 0;}",
  "threshold": 0.5
}
```

## Notes

- The app resolves model checkpoint from known paths under the project.
- If no checkpoint exists, the app raises a clear startup error with tried locations.
- Cached metrics (if available) are loaded from `eval_report.json`; otherwise metrics are computed on sampled test data.
