from flask import Flask, render_template, request, jsonify
import requests
import os
import textstat

app = Flask(__name__)

# ── Hugging Face Inference API ────────────────────────────────
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_TOKEN = os.environ.get("HF_TOKEN", "")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def summarize_article(text: str) -> str:
    """Summarize text using the Hugging Face Inference API."""
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 150,
            "min_length": 40,
            "do_sample": False,
        },
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    result = response.json()

    if isinstance(result, list) and len(result) > 0:
        return result[0].get("summary_text", "")
    return ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "").strip()

    if len(text) < 100:
        return jsonify({"error": "Please provide at least 100 characters."}), 400

    try:
        summary = summarize_article(text)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"HuggingFace API error: {str(e)}"}), 502

    if not summary:
        return jsonify({"error": "Failed to generate summary."}), 500

    return jsonify({
        "summary":             summary,
        "original_word_count": len(text.split()),
        "summary_word_count":  len(summary.split()),
        "compression_ratio":   round(len(summary.split()) / len(text.split()), 3),
        "readability_score":   round(textstat.flesch_reading_ease(summary), 2),
        "readability_grade":   textstat.text_standard(summary, float_output=False),
    })


if __name__ == "__main__":
    app.run(debug=True)
