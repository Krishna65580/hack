"""
Core reasoning engine for the Rural Health Assistant.

Design goals (mirrors the ElevanceSkills RAG bot architecture, adapted
for the hackathon problem statement):
- TF-IDF retrieval over a local, curated, non-diagnostic knowledge base
- Urgency/red-flag keyword detection -> escalation
- Lightweight multilingual detection (falls back gracefully offline)
- No definitive medical claims are ever generated - everything is
  templated from the KB, never free-generated, so the "non-diagnostic"
  constraint can never be violated by the model going off-script.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from knowledge_base import KB, EMERGENCY_CONTACTS, DISCLAIMER

try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

LANG_NAMES = {
    "en": "English", "hi": "Hindi", "te": "Telugu", "ta": "Tamil",
    "kn": "Kannada", "bn": "Bengali", "mr": "Marathi",
}

_CORPUS = [f"{e['topic']} {e['keywords']}" for e in KB]
_VECTORIZER = TfidfVectorizer(stop_words="english")
_TFIDF_MATRIX = _VECTORIZER.fit_transform(_CORPUS)


def detect_language(text: str) -> str:
    if not LANGDETECT_AVAILABLE or not text.strip():
        return "en"
    try:
        code = detect(text)
        return code if code in LANG_NAMES else "en"
    except Exception:
        return "en"


def check_urgency(query: str) -> list:
    """Scan query + matched entries for red-flag/urgent-care keywords."""
    q = query.lower()
    flags = []
    for entry in KB:
        for flag in entry.get("urgent_flags", []):
            if flag.lower() in q:
                flags.append((entry["topic"], flag))
    return flags


def retrieve(query: str, top_k: int = 1, threshold: float = 0.12):
    """Return best-matching KB entries for a query using TF-IDF cosine sim."""
    if not query.strip():
        return []
    q_vec = _VECTORIZER.transform([query])
    sims = cosine_similarity(q_vec, _TFIDF_MATRIX).flatten()
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    results = [(KB[i], score) for i, score in ranked[:top_k] if score >= threshold]
    return results


def build_response(query: str) -> dict:
    """
    Main entry point. Returns a structured, non-diagnostic response:
    {
        'language': str,
        'urgent': bool,
        'urgent_flags': [...],
        'matches': [(entry, score), ...],
        'text': str   # final rendered assistant message
    }
    """
    lang = detect_language(query)
    urgent_flags = check_urgency(query)
    matches = retrieve(query, top_k=1)

    lines = []

    if urgent_flags:
        topics = ", ".join(sorted({t for t, _ in urgent_flags}))
        lines.append(
            f"⚠️ Some words in your message ({topics}) may indicate a "
            f"situation that needs urgent medical attention. Please contact "
            f"emergency services or visit the nearest hospital right away."
        )
        lines.append(
            "Emergency numbers: " +
            ", ".join(f"{k}: {v}" for k, v in EMERGENCY_CONTACTS.items())
        )

    if matches:
        entry, score = matches[0]
        lines.append(f"**{entry['topic']}** — general information:")
        lines.append(entry["answer"])
    elif not urgent_flags:
        lines.append(
            "I don't have specific general information on that topic yet. "
            "For anything health-related that concerns you, the safest step "
            "is to speak with a doctor or visit a nearby health center — "
            "I can help you find one."
        )

    lines.append("")
    lines.append(DISCLAIMER)

    return {
        "language": lang,
        "language_name": LANG_NAMES.get(lang, "English"),
        "urgent": bool(urgent_flags),
        "urgent_flags": urgent_flags,
        "matches": matches,
        "text": "\n\n".join(lines),
    }
