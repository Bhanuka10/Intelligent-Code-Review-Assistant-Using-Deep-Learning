// ===== DOM ELEMENT CACHING =====
const codeInput = document.getElementById("codeInput");
const languageSelect = document.getElementById("languageSelect");
const fileInput = document.getElementById("fileInput");
const charCount = document.getElementById("charCount");
const clearCodeBtn = document.getElementById("clearCodeBtn");

const thresholdInput = document.getElementById("thresholdInput");
const thresholdValue = document.getElementById("thresholdValue");
const analyzeBtn = document.getElementById("analyzeBtn");

const statusEl = document.getElementById("status");
const statusBadge = document.getElementById("statusBadge");

const resultSection = document.getElementById("resultSection");
const resultBadge = document.getElementById("resultBadge");
const predictionBadge = document.getElementById("predictionBadge");
const predictionCard = document.getElementById("predictionCard");
const predictionText = document.getElementById("predictionText");
const confidenceGauge = document.getElementById("confidenceGauge");
const confidenceText = document.getElementById("confidenceText");
const defectProbText = document.getElementById("defectProbText");
const cleanProbText = document.getElementById("cleanProbText");

const topTokensList = document.getElementById("topTokensList");
const suggestionsList = document.getElementById("suggestionsList");

const metricsGrid = document.getElementById("metricsGrid");
const metricsMeta = document.getElementById("metricsMeta");
const refreshMetricsBtn = document.getElementById("refreshMetricsBtn");

const scanHistory = document.getElementById("scanHistory");
const historyEmpty = document.getElementById("historyEmpty");

// ===== STATE MANAGEMENT =====
let scanHistory_data = [];

// ===== UTILITY FUNCTIONS =====
function fmt(value, decimals = 4) {
	if (typeof value === "number") {
		const multiplier = Math.pow(10, decimals);
		return (Math.round(value * multiplier) / multiplier).toFixed(decimals);
	}
	return String(value);
}

function formatPercent(value) {
	return Math.round(value * 100) + "%";
}

function showStatus(message, type = "info") {
	statusEl.textContent = message;
	statusEl.className = `status-message show ${type}`;
	setTimeout(() => {
		statusEl.classList.remove("show");
	}, 5000);
}

function setLoadingState(isLoading) {
	analyzeBtn.disabled = isLoading;
	if (isLoading) {
		analyzeBtn.textContent = "⏳ Analyzing...";
		statusBadge.textContent = "Analyzing";
		statusBadge.classList.remove("error");
	} else {
		analyzeBtn.innerHTML = `<svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>Analyze Code`;
		statusBadge.textContent = "Ready";
		statusBadge.classList.remove("error");
	}
}

// ===== CODE EDITOR FEATURES =====
codeInput.addEventListener("input", () => {
	const count = codeInput.value.length;
	charCount.textContent = count.toLocaleString() + " characters";
});

clearCodeBtn.addEventListener("click", () => {
	codeInput.value = "";
	codeInput.focus();
	charCount.textContent = "0 characters";
	resultSection.classList.add("hidden");
});

fileInput.addEventListener("change", async (e) => {
	const file = e.target.files[0];
	if (!file) return;

	try {
		const text = await file.text();
		codeInput.value = text;
		charCount.textContent = text.length.toLocaleString() + " characters";
		showStatus(`File loaded: ${file.name}`, "success");
	} catch (error) {
		showStatus(`Error reading file: ${error.message}`, "error");
	}
});

// ===== THRESHOLD CONTROL =====
thresholdInput.addEventListener("input", () => {
	const val = parseFloat(thresholdInput.value);
	thresholdValue.textContent = fmt(val, 2);
});

// ===== RENDER RESULTS =====
function updateConfidenceGauge(confidence) {
	const percent = Math.min(100, Math.max(0, confidence * 100));
	confidenceGauge.style.width = percent + "%";
	confidenceText.textContent = formatPercent(confidence);
}

function renderPredictionCard(payload) {
	const isPredictDefect = payload.prediction.toUpperCase() === "DEFECTIVE";

	// Update badge
	predictionBadge.textContent = isPredictDefect ? "🚨 DEFECTIVE" : "✓ CLEAN";
	predictionBadge.className = isPredictDefect ? "prediction-badge" : "prediction-badge clean";

	// Update prediction text
	predictionText.textContent = isPredictDefect
		? "Code contains potential issues"
		: "Code appears to be clean";

	// Update confidence gauge
	updateConfidenceGauge(payload.confidence);

	// Update probabilities
	defectProbText.textContent = formatPercent(payload.defect_prob);
	cleanProbText.textContent = formatPercent(payload.clean_prob);

	// Update result badge
	resultBadge.className = "section-badge";
	resultBadge.textContent = isPredictDefect ? "⚠ Issues Detected" : "✓ No Issues";
}

function renderTokens(tokens) {
	topTokensList.innerHTML = "";

	if (!tokens || tokens.length === 0) {
		const li = document.createElement("li");
		li.textContent = "No significant tokens identified";
		topTokensList.appendChild(li);
		return;
	}

	tokens.slice(0, 12).forEach((item) => {
		const li = document.createElement("li");
		const score = fmt(item.score, 3);
		li.textContent = `${item.token}`;
		li.title = `Attribution score: ${score}`;
		topTokensList.appendChild(li);
	});
}

function renderSuggestions(suggestions) {
	suggestionsList.innerHTML = "";

	if (!suggestions || suggestions.length === 0) {
		const li = document.createElement("li");
		li.textContent = "No specific suggestions at this time.";
		suggestionsList.appendChild(li);
		return;
	}

	suggestions.forEach((text) => {
		const li = document.createElement("li");
		li.innerHTML = text.includes("<strong>") ? text : text;
		suggestionsList.appendChild(li);
	});
}

function renderResult(payload) {
	resultSection.classList.remove("hidden");
	renderPredictionCard(payload);
	renderTokens(payload.explainability?.top_tokens);
	renderSuggestions(payload.suggestions);

	// Add to history
	addToHistory(payload);

	// Scroll to results
	setTimeout(() => {
		resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
	}, 200);
}

// ===== ANALYSIS FUNCTION =====
async function analyzeCode() {
	const code = codeInput.value.trim();
	if (!code) {
		showStatus("Please paste code before analyzing.", "error");
		return;
	}

	setLoadingState(true);
	showStatus("Analyzing code with AI model...", "info");

	try {
		const response = await fetch("/analyze", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				code,
				threshold: parseFloat(thresholdInput.value),
			}),
		});

		const payload = await response.json();

		if (!response.ok) {
			throw new Error(payload.error || "Analysis request failed");
		}

		renderResult(payload);
		showStatus("Analysis complete!", "success");
	} catch (error) {
		showStatus("Error: " + error.message, "error");
		statusBadge.textContent = "Error";
		statusBadge.classList.add("error");
	} finally {
		setLoadingState(false);
	}
}

analyzeBtn.addEventListener("click", analyzeCode);
codeInput.addEventListener("keydown", (e) => {
	if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
		analyzeCode();
	}
});

// ===== METRICS RENDERING =====
function renderMetricsGrid(payload) {
	metricsGrid.innerHTML = "";

	// Main metrics cards
	const mainMetrics = [
		{ key: "accuracy", label: "Accuracy", color: "primary" },
		{ key: "precision", label: "Precision", color: "primary" },
		{ key: "recall", label: "Recall", color: "primary" },
		{ key: "f1_score", label: "F1 Score", color: "primary" },
	];

	mainMetrics.forEach(({ key, label }) => {
		const value = payload[key];
		const item = document.createElement("div");
		item.className = "metric-item";
		item.innerHTML = `
			<span class="metric-key">${label}</span>
			<span class="metric-value">${formatPercent(value)}</span>
		`;
		metricsGrid.appendChild(item);
	});

	// Confusion matrix
	if (payload.confusion_matrix) {
		const cmItem = document.createElement("div");
		cmItem.className = "metric-item wide confusion-matrix";

		const cm = payload.confusion_matrix;
		const cmHtml = `
			<div class="matrix-title">Confusion Matrix</div>
			<table class="matrix-table">
				<tr>
					<th></th>
					<th>Predicted Clean</th>
					<th>Predicted Defect</th>
				</tr>
				<tr>
					<th>Actual Clean</th>
					<td class="${cm[0][0] > cm[0][1] ? "high" : ""}">${cm[0][0]}</td>
					<td>${cm[0][1]}</td>
				</tr>
				<tr>
					<th>Actual Defect</th>
					<td>${cm[1][0]}</td>
					<td class="${cm[1][1] > cm[1][0] ? "high" : ""}">${cm[1][1]}</td>
				</tr>
			</table>
		`;
		cmItem.innerHTML = cmHtml;
		metricsGrid.appendChild(cmItem);
	}

	// Metadata
	let metaText = "Model Evaluation Metrics";
	if (payload.source) metaText += ` | Source: ${payload.source}`;
	if (payload.samples) metaText += ` | Samples: ${payload.samples}`;
	metricsMeta.textContent = metaText;
}

async function loadMetrics(recompute = false) {
	metricsMeta.textContent = "⏳ Loading metrics...";
	refreshMetricsBtn.disabled = true;

	try {
		const url = recompute ? "/metrics?recompute=true&max_samples=300" : "/metrics";
		const response = await fetch(url);
		const payload = await response.json();

		if (!response.ok) {
			throw new Error(payload.error || "Failed to load metrics");
		}

		renderMetricsGrid(payload);
	} catch (error) {
		metricsMeta.textContent = "❌ " + error.message;
	} finally {
		refreshMetricsBtn.disabled = false;
	}
}

refreshMetricsBtn.addEventListener("click", () => loadMetrics(true));

// ===== SCAN HISTORY =====
function addToHistory(result) {
	const item = {
		timestamp: new Date().toLocaleTimeString(),
		code: codeInput.value.substring(0, 50),
		prediction: result.prediction,
		confidence: result.confidence,
	};

	scanHistory_data.unshift(item);
	scanHistory_data = scanHistory_data.slice(0, 10); // Keep last 10
	updateHistoryDisplay();
}

function updateHistoryDisplay() {
	scanHistory.innerHTML = "";

	if (scanHistory_data.length === 0) {
		historyEmpty.style.display = "block";
		return;
	}

	historyEmpty.style.display = "none";

	scanHistory_data.forEach((item) => {
		const div = document.createElement("div");
		div.className = "scan-item";

		const isPredictDefect = item.prediction.toUpperCase() === "DEFECTIVE";
		const resultBg = isPredictDefect ? "defect" : "clean";

		div.innerHTML = `
			<div class="scan-item-info">
				<div class="scan-item-code">${escapeHtml(item.code)}...</div>
				<small style="color: var(--text-tertiary);">${item.timestamp}</small>
			</div>
			<div class="scan-item-result ${resultBg === "clean" ? "clean" : ""}">
				${item.prediction} (${formatPercent(item.confidence)})
			</div>
		`;

		scanHistory.appendChild(div);
	});
}

function escapeHtml(text) {
	const map = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
		'"': "&quot;",
		"'": "&#039;",
	};
	return text.replace(/[&<>"']/g, (m) => map[m]);
}

// ===== INITIALIZATION =====
document.addEventListener("DOMContentLoaded", () => {
	loadMetrics(false);
	updateHistoryDisplay();
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener("keydown", (e) => {
	// Ctrl/Cmd + K to focus code input
	if ((e.ctrlKey || e.metaKey) && e.key === "k") {
		e.preventDefault();
		codeInput.focus();
	}
});
