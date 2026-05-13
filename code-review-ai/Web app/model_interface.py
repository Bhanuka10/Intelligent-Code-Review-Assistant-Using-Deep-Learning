from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from transformers import AutoModel, AutoTokenizer


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CodeReviewModel(nn.Module):
	def __init__(self, model_name: str, num_labels: int = 2, dropout: float = 0.3):
		super().__init__()
		self.encoder = AutoModel.from_pretrained(model_name)
		hidden_size = self.encoder.config.hidden_size
		self.classifier = nn.Sequential(
			nn.Dropout(dropout),
			nn.Linear(hidden_size, 256),
			nn.ReLU(),
			nn.Dropout(dropout),
			nn.Linear(256, num_labels),
		)

	def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
		out = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
		return self.classifier(out.last_hidden_state[:, 0, :])


def _first_existing_path(candidates: list[Path]) -> Path | None:
	for path in candidates:
		if path.exists():
			return path
	return None


class CodeReviewAssistant:
	def __init__(
		self,
		model_name: str = "microsoft/codebert-base",
		max_length: int = 512,
		batch_size: int = 16,
	):
		self.model_name = model_name
		self.max_length = max_length
		self.batch_size = batch_size
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

		tokenizer_path = _first_existing_path(
			[
				PROJECT_ROOT / "tokenizer",
				PROJECT_ROOT / "notebooks" / "tokenizer",
			]
		)
		if tokenizer_path is None:
			raise FileNotFoundError("Tokenizer folder not found in expected locations.")

		self.tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path))
		self.model = CodeReviewModel(model_name).to(self.device)

		checkpoint_path = self.resolve_checkpoint_path()
		self.model.load_state_dict(torch.load(checkpoint_path, map_location=self.device))
		self.model.eval()
		self.checkpoint_path = checkpoint_path

	def resolve_checkpoint_path(self) -> Path:
		checkpoint_candidates = [
			PROJECT_ROOT / ".gitignore" / "checkpoints" / "best_model.pt",
			PROJECT_ROOT / "checkpoints" / "best_model.pt",
			PROJECT_ROOT / "notebooks" / "checkpoints" / "best_model.pt",
		]
		checkpoint_path = _first_existing_path(checkpoint_candidates)
		if checkpoint_path is None:
			tried = ", ".join(str(path) for path in checkpoint_candidates)
			raise FileNotFoundError(f"Could not find best_model.pt. Tried: {tried}")
		return checkpoint_path

	def _encode(self, code: str) -> dict[str, torch.Tensor]:
		enc = self.tokenizer(
			code,
			max_length=self.max_length,
			padding="max_length",
			truncation=True,
			return_tensors="pt",
		)
		return {
			"input_ids": enc["input_ids"].to(self.device),
			"attention_mask": enc["attention_mask"].to(self.device),
		}

	def predict(self, code: str, threshold: float = 0.5) -> dict[str, Any]:
		features = self._encode(code)
		with torch.no_grad():
			logits = self.model(features["input_ids"], features["attention_mask"])
			probs = F.softmax(logits, dim=1).squeeze(0)

		clean_prob = float(probs[0].item())
		defect_prob = float(probs[1].item())
		prediction = "DEFECTIVE" if defect_prob >= threshold else "CLEAN"
		confidence = defect_prob if prediction == "DEFECTIVE" else clean_prob

		return {
			"prediction": prediction,
			"clean_prob": clean_prob,
			"defect_prob": defect_prob,
			"confidence": float(confidence),
			"threshold": float(threshold),
		}

	def explain(self, code: str, target_class: int = 1, top_k: int = 12) -> dict[str, Any]:
		features = self._encode(code)
		input_ids = features["input_ids"]
		attention_mask = features["attention_mask"]

		embeddings = self.model.encoder.embeddings.word_embeddings(input_ids)
		embeddings = embeddings.detach().clone().requires_grad_(True)

		self.model.zero_grad(set_to_none=True)
		out = self.model.encoder(inputs_embeds=embeddings, attention_mask=attention_mask)
		logits = self.model.classifier(out.last_hidden_state[:, 0, :])
		probs = F.softmax(logits, dim=1)
		probs[:, target_class].sum().backward()

		grads = embeddings.grad
		if grads is None:
			return {"tokens": [], "scores": [], "top_tokens": []}

		token_scores = (grads * embeddings).sum(dim=-1).squeeze(0)
		token_scores = token_scores.detach().cpu().numpy()

		real_len = int(attention_mask.sum().item())
		token_ids = input_ids[0, :real_len].detach().cpu().numpy().tolist()
		tokens = self.tokenizer.convert_ids_to_tokens(token_ids)
		scores = token_scores[:real_len]

		max_abs = float(np.max(np.abs(scores))) if len(scores) > 0 else 1.0
		max_abs = max(max_abs, 1e-8)
		norm_scores = [float(score / max_abs) for score in scores]

		top_tokens = []
		special_tokens = set(self.tokenizer.all_special_tokens)
		sortable = []
		for index, (token, score) in enumerate(zip(tokens, norm_scores)):
			if token in special_tokens:
				continue
			sortable.append({"index": index, "token": token, "score": score, "abs_score": abs(score)})

		sortable.sort(key=lambda item: item["abs_score"], reverse=True)
		for item in sortable[:top_k]:
			top_tokens.append(
				{
					"index": item["index"],
					"token": item["token"],
					"score": float(item["score"]),
				}
			)

		return {
			"tokens": tokens,
			"scores": norm_scores,
			"top_tokens": top_tokens,
		}

	def suggest(self, code: str, defect_prob: float, top_tokens: list[dict[str, Any]]) -> list[str]:
		suggestions: list[str] = []
		lowered = code.lower()

		high_risk_patterns = {
			r"\bstrcpy\s*\(": "Potential buffer overflow risk (`strcpy`). Consider safer bounded copy functions.",
			r"\bgets\s*\(": "Unsafe input API (`gets`) detected. Replace with bounded input handling.",
			r"\bmalloc\s*\(": "Dynamic allocation detected. Verify corresponding `free` paths to avoid leaks.",
			r"\bwhile\s*\(\s*1\s*\)": "Infinite loop pattern detected. Ensure explicit break/timeout conditions.",
		}

		for pattern, message in high_risk_patterns.items():
			if re.search(pattern, lowered):
				suggestions.append(message)

		line_count = len(code.splitlines())
		if line_count > 80:
			suggestions.append("Function appears long. Consider splitting into smaller units for readability and testability.")

		branch_count = len(re.findall(r"\b(if|else if|switch|for|while)\b", lowered))
		if branch_count > 10:
			suggestions.append("High branching complexity detected. Consider simplifying control flow.")

		if defect_prob >= 0.7:
			suggestions.append("Model confidence is high for a defect. Prioritize this snippet for manual review.")
		elif defect_prob >= 0.5:
			suggestions.append("Model indicates moderate defect risk. Review highlighted tokens and edge cases.")
		else:
			suggestions.append("Model predicts low defect risk. Still run static analysis and tests for coverage.")

		if top_tokens:
			top_text = ", ".join(token_info["token"] for token_info in top_tokens[:5])
			suggestions.append(f"Most influential tokens: {top_text}")

		return suggestions

	def analyze_code(self, code: str, threshold: float = 0.5) -> dict[str, Any]:
		prediction = self.predict(code, threshold=threshold)
		explanation = self.explain(code, target_class=1)
		suggestions = self.suggest(code, prediction["defect_prob"], explanation["top_tokens"])
		return {
			**prediction,
			"explainability": explanation,
			"suggestions": suggestions,
		}

	def load_cached_metrics(self) -> dict[str, Any] | None:
		candidates = [
			PROJECT_ROOT / "notebooks" / "checkpoints" / "eval_report.json",
			PROJECT_ROOT / "checkpoints" / "eval_report.json",
			PROJECT_ROOT / ".gitignore" / "checkpoints" / "eval_report.json",
		]
		metrics_path = _first_existing_path(candidates)
		if metrics_path is None:
			return None
		with metrics_path.open("r", encoding="utf-8") as file:
			payload = json.load(file)
		payload["source"] = str(metrics_path)
		payload["mode"] = "cached"
		return payload

	def evaluate(self, max_samples: int = 300) -> dict[str, Any]:
		data_candidates = [
			PROJECT_ROOT / "notebooks" / "data" / "test_clean.csv",
			PROJECT_ROOT / "data" / "test_clean.csv",
		]
		data_path = _first_existing_path(data_candidates)
		if data_path is None:
			tried = ", ".join(str(path) for path in data_candidates)
			raise FileNotFoundError(f"Could not find test_clean.csv. Tried: {tried}")

		dataframe = pd.read_csv(data_path)
		if max_samples and len(dataframe) > max_samples:
			dataframe = dataframe.sample(n=max_samples, random_state=42).reset_index(drop=True)

		labels = dataframe["target"].astype(int).to_numpy()
		codes = dataframe["clean_code"].astype(str).tolist()

		predictions: list[int] = []
		probabilities: list[float] = []
		self.model.eval()

		for start in range(0, len(codes), self.batch_size):
			batch_codes = codes[start : start + self.batch_size]
			encoded = self.tokenizer(
				batch_codes,
				max_length=self.max_length,
				padding="max_length",
				truncation=True,
				return_tensors="pt",
			)
			input_ids = encoded["input_ids"].to(self.device)
			attention_mask = encoded["attention_mask"].to(self.device)

			with torch.no_grad():
				logits = self.model(input_ids, attention_mask)
				probs = F.softmax(logits, dim=1)

			predictions.extend(torch.argmax(probs, dim=1).detach().cpu().numpy().tolist())
			probabilities.extend(probs[:, 1].detach().cpu().numpy().tolist())

		cm = confusion_matrix(labels, predictions)
		report = {
			"accuracy": float(accuracy_score(labels, predictions)),
			"precision": float(precision_score(labels, predictions, zero_division=0)),
			"recall": float(recall_score(labels, predictions, zero_division=0)),
			"f1_score": float(f1_score(labels, predictions, zero_division=0)),
			"confusion_matrix": cm.tolist(),
			"samples": int(len(labels)),
			"mode": "computed",
			"data_path": str(data_path),
		}
		return report
