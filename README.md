# 🤖 AI Writer & Summarizer

> **Abstractive text summarization** powered by BART (facebook/bart-large-cnn), served through a Flask web app with a sleek dark-themed UI.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/BART-large--CNN-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white" />
  <img src="https://img.shields.io/badge/Dataset-CNN--DailyMail-E74C3C?style=for-the-badge" />
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📝 **Abstractive Summarization** | Generate human-like summaries using BART beam search |
| 📊 **Analytics Dashboard** | Word counts, compression ratio, Flesch readability score & grade |
| 🔀 **Sample Articles** | Load random CNN-DailyMail test articles with ground-truth references |
| 📋 **Comparison View** | Side-by-side generated vs reference summary |
| ⚡ **Chunking Engine** | Handles long articles (>1024 tokens) via smart splitting |
| 🎨 **Dark Glassmorphism UI** | Modern dark theme with gradient orbs, glass cards & micro-animations |

---

## �️ Demo

<!-- Replace with your own screenshot -->
<!-- ![App Screenshot](screenshots/demo.png) -->

```
Paste any article → Click "Summarize" → Get instant summary + analytics
```

---

## 📁 Project Structure

```
AI-Writer-Summarizer/
├── app.py                   # Flask server — 3 API routes
├── cnn_summarizer.py        # BART model loader + summarize_article()
├── requirements.txt         # Python dependencies
├── README.md
├── workflow.drawio           # Architecture diagram (draw.io)
├── templates/
│   └── index.html           # Jinja2 template — dark themed UI
└── static/
    ├── css/style.css        # Glassmorphism design system
    └── js/app.js            # Frontend logic (fetch, loading states)
```

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/AI-Writer-Summarizer.git
cd AI-Writer-Summarizer
```

### 2. Set up virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download dataset *(optional — for "Load Sample" button)*

```bash
pip install kagglehub
python -c "import kagglehub; kagglehub.dataset_download('gowrishankarp/newspaper-text-summarization-cnn-dailymail')"
```

### 5. Run

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser 🚀

> **Note:** First launch downloads the BART model (~1.6 GB) from HuggingFace.

---

## 📡 API Reference

### `POST /summarize`

Summarize article text.

**Request:**
```json
{
  "text": "Your article here (min 100 characters)..."
}
```

**Response:**
```json
{
  "summary": "Generated summary...",
  "original_word_count": 450,
  "summary_word_count": 55,
  "compression_ratio": 0.122,
  "readability_score": 52.3,
  "readability_grade": "10th and 11th grade"
}
```

### `GET /sample`

Returns a random CNN-DailyMail article with its reference summary.

---

## 🧠 How It Works

```
Article Text
    │
    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Chunk Text  │────▶│  Tokenize    │────▶│  BART Model  │
│  (≤900 words)│     │  (max 1024)  │     │  Beam Search │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                                  ▼
                                          ┌──────────────┐
                                          │  Decode &    │
                                          │  Join Parts  │
                                          └──────┬───────┘
                                                  │
                                                  ▼
                                         Summary + Stats
```

---

## 📊 Evaluation Results

Tested on 20 CNN-DailyMail articles:

| Metric | Score |
|--------|-------|
| **ROUGE-1** | 0.4408 |
| **ROUGE-2** | 0.2204 |
| **ROUGE-L** | 0.3233 |
| **Avg Compression** | ~12% |
| **Avg Time/Article** | 1.5s (GPU) |

---

## 🛠️ Tech Stack

- **Backend:** Flask, Python 3.10+
- **Model:** `facebook/bart-large-cnn` via HuggingFace Transformers
- **Frontend:** HTML5, Vanilla CSS (glassmorphism), Vanilla JS
- **Analytics:** `textstat` (Flesch reading ease, grade level)
- **Dataset:** CNN-DailyMail (Kaggle — 11,490 test articles)

---

## 🤝 Contributing

1. Fork the repository
2. Create your branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is for **educational purposes**. The BART model is released by Meta under the MIT License.

---

<p align="center">
  Made with ❤️ using Flask & HuggingFace Transformers
</p>
