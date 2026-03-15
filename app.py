from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from cnn_summarizer import summarize_article
import textstat

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "").strip()

    if len(text) < 100:
        return jsonify({"error": "Please provide at least 100 characters."}), 400

    summary = summarize_article(text)

    return jsonify({
        "summary":             summary,
        "original_word_count": len(text.split()),
        "summary_word_count":  len(summary.split()),
        "compression_ratio":   round(len(summary.split()) / len(text.split()), 3),
        "readability_score":   round(textstat.flesch_reading_ease(summary), 2),
        "readability_grade":   textstat.text_standard(summary, float_output=False),
    })


# ── Load a random CNN-DailyMail sample for demo ──────────────
@app.route("/sample")
def sample():
    csv_path = os.path.join(
        os.path.expanduser("~"),
        ".cache", "kagglehub", "datasets", "gowrishankarp",
        "newspaper-text-summarization-cnn-dailymail", "versions", "2",
        "cnn_dailymail", "test.csv"
    )
    if not os.path.isfile(csv_path):
        return jsonify({"error": "Sample dataset (cnn_dailymail/test.csv) not found."}), 404

    df  = pd.read_csv(csv_path).dropna()
    row = df.sample(1).iloc[0]
    return jsonify({
        "article":   row["article"],
        "reference": row["highlights"],
    })


if __name__ == "__main__":
    app.run(debug=True)
