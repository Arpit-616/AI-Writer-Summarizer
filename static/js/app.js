// ── DOM refs ────────────────────────────────────────────
const inputEl       = document.getElementById("article-input");
const charCountEl   = document.getElementById("char-count");
const btnSummarize  = document.getElementById("btn-summarize");
const btnSample     = document.getElementById("btn-sample");
const resultCard    = document.getElementById("result-card");
const summaryTextEl = document.getElementById("summary-text");
const referenceBox  = document.getElementById("reference-box");
const referenceText = document.getElementById("reference-text");
const toastEl       = document.getElementById("toast");

// stat spans
const statOriginal    = document.getElementById("stat-original");
const statSummary     = document.getElementById("stat-summary");
const statCompression = document.getElementById("stat-compression");
const statReadability = document.getElementById("stat-readability");
const statGrade       = document.getElementById("stat-grade");

let toastTimer = null;

// ── Character counter ──────────────────────────────────
inputEl.addEventListener("input", () => {
  const len = inputEl.value.length;
  charCountEl.textContent = `${len.toLocaleString()} character${len !== 1 ? "s" : ""}`;
});

// ── Toast helper ───────────────────────────────────────
function showToast(msg, duration = 3500) {
  toastEl.textContent = msg;
  toastEl.classList.add("toast--show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove("toast--show"), duration);
}

// ── Summarize ──────────────────────────────────────────
async function summarize() {
  const text = inputEl.value.trim();
  if (text.length < 100) {
    showToast("⚠ Please enter at least 100 characters.");
    return;
  }

  // loading state
  btnSummarize.classList.add("btn--loading");
  btnSummarize.disabled = true;

  try {
    const res  = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();

    if (!res.ok) {
      showToast(data.error || "Something went wrong.");
      return;
    }

    // populate results
    summaryTextEl.textContent   = data.summary;
    statOriginal.textContent    = data.original_word_count;
    statSummary.textContent     = data.summary_word_count;
    statCompression.textContent = `${(data.compression_ratio * 100).toFixed(1)}%`;
    statReadability.textContent = data.readability_score;
    statGrade.textContent       = data.readability_grade;

    resultCard.classList.remove("hidden");
    resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    showToast("Network error — is the server running?");
    console.error(err);
  } finally {
    btnSummarize.classList.remove("btn--loading");
    btnSummarize.disabled = false;
  }
}

// ── Load Sample ────────────────────────────────────────
async function loadSample() {
  btnSample.disabled = true;
  btnSample.textContent = "⏳ Loading…";

  try {
    const res  = await fetch("/sample");
    const data = await res.json();

    if (!res.ok) {
      showToast(data.error || "Could not load sample.");
      return;
    }

    inputEl.value = data.article;
    inputEl.dispatchEvent(new Event("input"));

    // show reference for later comparison
    if (data.reference) {
      referenceText.textContent = data.reference;
      referenceBox.classList.remove("hidden");
    }
  } catch (err) {
    showToast("Network error — is the server running?");
    console.error(err);
  } finally {
    btnSample.disabled = false;
    btnSample.textContent = "↻ Load Sample Article";
  }
}
