"""
CNN-DailyMail Article Summarizer
Uses facebook/bart-large-cnn for abstractive text summarization.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ── Load model & tokenizer once at import ────────────────────
print("⏳ Loading BART model and tokenizer …")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model     = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(f"✅ Model loaded on {device.upper()}")


def _chunk_text(text: str, max_tokens: int = 900) -> list[str]:
    """Split long text into word-level chunks BART can handle."""
    words  = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i : i + max_tokens])
        if len(chunk.strip()) >= 50:
            chunks.append(chunk)
    return chunks


def summarize_article(article: str) -> str:
    """
    Summarize an article using BART with chunking support.
    Long articles are split into ≤900-word chunks; each chunk is
    summarised independently and the results are joined.
    """
    chunks           = _chunk_text(article)
    partial_summaries = []

    for chunk in chunks:
        inputs = tokenizer(
            [chunk],
            max_length=1024,
            return_tensors="pt",
            truncation=True,
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}

        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=4,
            max_length=150,
            min_length=40,
            early_stopping=True,
        )
        partial_summaries.append(
            tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        )

    return " ".join(partial_summaries)
