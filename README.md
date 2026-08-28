# Rural Health Assistant

**HackSprint 2.0 — Problem Statement #2: Healthcare Accessibility and Rural Health Assistant**

A non-diagnostic digital healthcare assistance platform. It helps users
understand general health information, locate nearby healthcare
resources, and manage basic healthcare activities — without ever
diagnosing a condition or prescribing treatment.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

- `knowledge_base.py` — curated, non-diagnostic health topics. Every
  entry is educational only and ends by pointing to a professional.
  Swap-in point for a licensed medical content API in production.
- `engine.py` — TF-IDF retrieval (scikit-learn) over the knowledge
  base, red-flag/urgency keyword detection for escalation, and
  language detection (`langdetect`). Responses are always templated
  from the KB — the system can never free-generate a diagnostic claim.
- `locator.py` — nearby healthcare facility search. Static demo data;
  the function signature is designed as a drop-in swap for a real
  Places/Overpass API call using live coordinates.
- `app.py` — Streamlit UI: chat, facility locator, reminders, and a
  private local notes space.

## Why this is safe by design

The "non-diagnostic" constraint isn't a prompt instruction that an LLM
could ignore — it's structural. Every chat response comes from a fixed,
human-reviewed KB entry (or an urgent-care escalation message). There
is no free-text generation path that could produce a diagnosis or a
dosage recommendation.

## Features implemented (vs. problem statement)

- [x] Health-information guidance (non-diagnostic, templated)
- [x] Nearby hospital/health-center locator
- [x] Emergency contact functionality
- [x] Medicine/appointment reminders
- [x] Patient health-record organization (local notes)
- [x] Multilingual detection hook (`langdetect`)
- [x] Voice interaction hook (UI stub — wire to STT/TTS API)
- [x] Escalation to healthcare professionals (urgency keyword detection)

## Roadmap for the demo

1. Wire the 🎤 Speak button to the browser's Web Speech API or a
   cloud STT service.
2. Swap `locator.py`'s static data for a live Places/Overpass API call.
3. Expand `knowledge_base.py` with more topics/localized languages as
   time allows.
