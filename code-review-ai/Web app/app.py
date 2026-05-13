from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from model_interface import CodeReviewAssistant


app = Flask(__name__, template_folder="Template", static_folder="Static")
assistant = CodeReviewAssistant()


@app.get("/")
def index():
	return render_template("Index.html")


@app.post("/analyze")
def analyze():
	payload = request.get_json(silent=True) or request.form
	code = (payload.get("code") or "").strip()
	threshold = payload.get("threshold", 0.5)

	if not code:
		return jsonify({"error": "Please provide source code to analyze."}), 400

	try:
		threshold_value = float(threshold)
	except (TypeError, ValueError):
		threshold_value = 0.5

	threshold_value = max(0.0, min(1.0, threshold_value))
	result = assistant.analyze_code(code, threshold=threshold_value)
	return jsonify(result)


@app.get("/metrics")
def metrics():
	max_samples_arg = request.args.get("max_samples")
	try:
		max_samples = int(max_samples_arg) if max_samples_arg else 300
	except (TypeError, ValueError):
		max_samples = 300

	if request.args.get("recompute", "false").lower() != "true":
		cached = assistant.load_cached_metrics()
		if cached is not None:
			return jsonify(cached)

	report = assistant.evaluate(max_samples=max_samples)
	return jsonify(report)


@app.get("/health")
def health():
	return jsonify(
		{
			"status": "ok",
			"device": str(assistant.device),
			"checkpoint": str(assistant.checkpoint_path),
			"model": assistant.model_name,
		}
	)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=7860, debug=True)
