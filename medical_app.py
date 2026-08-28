"""
Rural Health Assistant — HackSprint 2.0
Problem Statement #2: Healthcare Accessibility and Rural Health Assistant

A non-diagnostic digital healthcare assistance platform that helps users
understand general health information, locate nearby healthcare resources,
and manage basic healthcare activities (reminders). This system does NOT
diagnose or prescribe — it's powered by an LLM that is tightly prompted to
stay non-diagnostic, and every response routes serious concerns to real
medical professionals and emergency services.
"""

import uuid
import streamlit as st
from datetime import datetime, date
from engine import stream_response, build_response
from locator import search_facilities
from knowledge_base import EMERGENCY_CONTACTS, DISCLAIMER

st.set_page_config(
    page_title="Rural Health Assistant",
    page_icon="⚕️",
    layout="wide",
)

# ---------- ChatGPT-style polish ----------
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; max-width: 900px; }
    [data-testid="stChatMessage"] { padding: 0.25rem 0; }
    .urgent-banner {
        background: #fee2e2; border: 1px solid #fca5a5; color: #7f1d1d;
        padding: 0.9rem 1.1rem; border-radius: 10px; margin-bottom: 0.6rem;
        font-weight: 600;
    }
    .stChatInput { position: sticky; bottom: 0; }
</style>
""", unsafe_allow_html=True)

URGENT_BANNER_HTML = (
    "<div class='urgent-banner'>🚨 This may be urgent — "
    "call 108 (Ambulance) or 112 (Emergency) now, or go "
    "to the nearest hospital.</div>"
)

# ---------- session state ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [{"role": "user"/"assistant", "text": str, "urgent": bool}]
if "reminders" not in st.session_state:
    st.session_state.reminders = []
if "records" not in st.session_state:
    st.session_state.records = []

# ---------- sidebar: emergency + navigation ----------
with st.sidebar:
    st.markdown("## ⚕️ Rural Health Assistant")
    st.caption("Non-diagnostic healthcare accessibility platform")

    st.markdown("### 🚨 Emergency Contacts")
    for name, number in EMERGENCY_CONTACTS.items():
        st.markdown(f"**{name}:** `{number}`")

    st.divider()
    page = st.radio(
        "Navigate",
        ["💬 Health Info Chat", "🏥 Find Healthcare", "⏰ Reminders", "📋 My Health Notes"],
        label_visibility="collapsed",
    )

    if page == "💬 Health Info Chat" and st.session_state.chat_history:
        st.divider()
        if st.button("🗑️ New chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    st.divider()
    st.caption("Built for HackSprint 2.0 — Dept. of CSE, AITAM")

# ---------- header disclaimer (always visible) ----------
st.info(DISCLAIMER, icon="⚕️")

# ================= PAGE 1: CHAT =================
if page == "💬 Health Info Chat":
    st.title("Health Information Assistant")
    st.caption("Ask about common symptoms or health topics, in your own words and language.")

    # Welcome message + quick topics, shown only before the first question
    if not st.session_state.chat_history:
        st.success(
            "👋 **Welcome!** I'm here to give you general health information, "
            "help you find nearby care, and flag anything that needs urgent "
            "attention. Type a question below, or tap a topic to try it out."
        )
        st.caption("Quick topics")
        suggestions = ["Fever", "Cough and cold", "Loose motions", "Headache",
                        "Skin rash", "Feeling stressed", "Child health", "Pregnancy care"]
        cols = st.columns(4)
        clicked = None
        for i, s in enumerate(suggestions):
            with cols[i % 4]:
                if st.button(s, use_container_width=True, key=f"sugg_{i}"):
                    clicked = s
        if clicked:
            st.session_state.chat_history.append({"role": "user", "text": clicked})
            st.rerun()

    # Render existing history as chat bubbles
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑"):
                st.markdown(msg["text"])
        else:
            with st.chat_message("assistant", avatar="⚕️"):
                if msg.get("urgent"):
                    st.markdown(URGENT_BANNER_HTML, unsafe_allow_html=True)
                st.markdown(msg["text"])

    # If the last message is from the user with no reply yet, generate one now
    needs_reply = (
        st.session_state.chat_history
        and st.session_state.chat_history[-1]["role"] == "user"
    )
    if needs_reply:
        latest = st.session_state.chat_history[-1]["text"]
        history_so_far = st.session_state.chat_history[:-1]
        with st.chat_message("assistant", avatar="⚕️"):
            placeholder = st.empty()
            urgent_placeholder = st.empty()
            full_text = ""
            urgent_shown = False
            for chunk in stream_response(history_so_far, latest):
                # Guard: don't assume engine.py has set these attributes yet.
                # Reading an unset attribute here would raise AttributeError
                # on the very first message of the app's lifetime.
                if getattr(stream_response, "last_urgent", False) and not urgent_shown:
                    urgent_placeholder.markdown(URGENT_BANNER_HTML, unsafe_allow_html=True)
                    urgent_shown = True
                full_text += chunk
                placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
        st.session_state.chat_history.append({
            "role": "assistant",
            "text": getattr(stream_response, "last_full_text", None) or full_text,
            "urgent": getattr(stream_response, "last_urgent", False),
        })
        st.rerun()

    # Chat input pinned at the bottom, ChatGPT-style
    query = st.chat_input("Message Rural Health Assistant…")
    if query and query.strip():
        st.session_state.chat_history.append({"role": "user", "text": query.strip()})
        st.rerun()

# ================= PAGE 2: LOCATOR =================
elif page == "🏥 Find Healthcare":
    st.title("Find Nearby Healthcare")
    st.caption("Showing facilities near Tekkali, Andhra Pradesh (demo data — swap for live Places API in production)")

    search_q = st.text_input("Search by need (e.g. 'emergency', 'maternity', 'pediatric')", "")
    results = search_facilities(search_q)

    for f in results:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {f['name']}")
                st.markdown(f"**Type:** {f['type']}  |  **Services:** {f['services']}")
                st.markdown(f"📞 {f['phone']}")
            with c2:
                st.metric("Distance", f"{f['distance_km']} km")

# ================= PAGE 3: REMINDERS =================
elif page == "⏰ Reminders":
    st.title("Medicine & Appointment Reminders")

    with st.form("add_reminder", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            r_title = st.text_input("What (medicine / appointment)")
        with c2:
            r_date = st.date_input("Date", min_value=date.today())
        with c3:
            r_time = st.time_input("Time")
        submitted = st.form_submit_button("Add Reminder", type="primary")
        if submitted:
            # clear_on_submit wipes the form regardless of validity, so we
            # must give explicit feedback rather than failing silently.
            if not r_title.strip():
                st.error("Please enter what the reminder is for.")
            else:
                st.session_state.reminders.append({
                    "id": uuid.uuid4().hex,
                    "title": r_title, "date": str(r_date), "time": str(r_time),
                    "added": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                st.success(f"Reminder added: {r_title} on {r_date} at {r_time}")

    st.divider()
    if not st.session_state.reminders:
        st.caption("No reminders yet.")
    else:
        sorted_reminders = sorted(st.session_state.reminders, key=lambda r: (r["date"], r["time"]))
        for r in sorted_reminders:
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"**{r['title']}** — {r['date']} at {r['time']}")
            with c2:
                # Key/removal by stable id, not list position — avoids
                # deleting the wrong entry when reminders share the same
                # title/date/time, and avoids widget-key churn on re-sort.
                if st.button("✕", key=f"del_{r['id']}"):
                    st.session_state.reminders = [
                        x for x in st.session_state.reminders if x["id"] != r["id"]
                    ]
                    st.rerun()

# ================= PAGE 4: HEALTH NOTES =================
elif page == "📋 My Health Notes":
    st.title("My Health Notes")
    st.caption(
        "A private, local space to jot down symptoms, visit summaries, or "
        "questions to ask your doctor. This is organizational only — not a "
        "medical record and not shared with anyone."
    )

    with st.form("add_note", clear_on_submit=True):
        note = st.text_area("New note")
        submitted = st.form_submit_button("Save Note", type="primary")
        if submitted:
            if not note.strip():
                st.error("Note can't be empty.")
            else:
                st.session_state.records.append({
                    "id": uuid.uuid4().hex,
                    "text": note, "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                st.success("Note saved.")

    st.divider()
    if not st.session_state.records:
        st.caption("No notes yet.")
    else:
        for rec in reversed(st.session_state.records):
            with st.container(border=True):
                st.caption(rec["date"])
                st.write(rec["text"])
