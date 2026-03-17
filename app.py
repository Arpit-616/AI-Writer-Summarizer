from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import textstat

load_dotenv()

app = Flask(__name__)

# ── Hugging Face API Setup ─────────────────────────────
HF_TOKEN = os.environ.get("HF_TOKEN", "")

if HF_TOKEN:
    print(f"✅ HF_TOKEN loaded (starts with {HF_TOKEN[:8]}...)")
else:
    print("⚠️ WARNING: HF_TOKEN is empty! Set it in Render environment.")

API_URL = "https://router.huggingface.co/hf-inference/models/sshleifer/distilbart-cnn-12-6"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# ── Summarization Function ─────────────────────────────
def summarize_article(text: str) -> str:
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 150,
            "min_length": 40
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    # Safe handling
    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]
    else:
        raise Exception(f"Unexpected response: {data}")


# ── Sample Data ─────────────────────────────
SAMPLE_ARTICLE = (
    "Scientists have discovered a new species of deep-sea fish in the Mariana Trench, "
    "the deepest part of the world's oceans. The fish, which has been named Pseudoliparis "
    "swirei, was found at a depth of approximately 8,000 meters. Researchers from the "
    "University of Washington used specially designed traps to capture several specimens "
    "during an expedition in 2014. The small, translucent fish belongs to the snailfish "
    "family and has adapted to survive extreme pressure, near-freezing temperatures, and "
    "complete darkness. Unlike many deep-sea creatures, it lacks the bioluminescent "
    "features common at such depths. The discovery sheds new light on the limits of "
    "vertebrate life and could help scientists understand how organisms adapt to extreme "
    "environments. The findings were published in the journal Zootaxa and have attracted "
    "widespread attention from the marine biology community. Further expeditions are "
    "planned to study the fish's behavior and ecology in its natural habitat."
)

SAMPLE_REFERENCE = (
    "A new deep-sea fish species, Pseudoliparis swirei, was discovered in the Mariana "
    "Trench at 8,000 meters depth. The translucent snailfish survives extreme pressure "
    "and darkness without bioluminescence. The discovery advances understanding of "
    "vertebrate life in extreme environments."
)

# ── Routes ─────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sample")
def sample():
    return jsonify({
        "article": SAMPLE_ARTICLE,
        "reference": SAMPLE_REFERENCE
    })


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "").strip()

    if len(text) < 100:
        return jsonify({"error": "Please provide at least 100 characters."}), 400

    try:
        summary = summarize_article(text)
    except Exception as e:
        return jsonify({"error": f"HuggingFace API error: {str(e)}"}), 502

    if not summary:
        return jsonify({"error": "Failed to generate summary."}), 500

    return jsonify({
        "summary": summary,
        "original_word_count": len(text.split()),
        "summary_word_count": len(summary.split()),
        "compression_ratio": round(len(summary.split()) / len(text.split()), 3),
        "readability_score": round(textstat.flesch_reading_ease(summary), 2),
        "readability_grade": textstat.text_standard(summary, float_output=False),
    })


# ── Run App (Render compatible) ─────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)